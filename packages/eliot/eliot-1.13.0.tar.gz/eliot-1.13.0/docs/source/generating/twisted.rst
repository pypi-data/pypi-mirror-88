Using Eliot with Twisted
========================

Eliot provides a variety of APIs to support integration with the `Twisted`_ networking framework.

.. _Twisted: https://twistedmatrix.com


.. _ThreadedWriter:

Non-blocking Destinations
-------------------------

``eliot.logwriter.ThreadedWriter`` is a logging destination that wraps a blocking destination and writes to it in a non-reactor thread.
This is useful because it keeps the Twisted reactor from blocking, e.g. if you're writing to a log file and the hard drive is overloaded.
``ThreadedWriter`` is a Twisted ``Service`` and starting it will call ``add_destinations`` for you and stopping it will call ``remove_destination``; there is no need to call those directly.

.. literalinclude:: ../../../examples/logfile.py

If you want log rotation you can pass in an ``eliot.FileDestination`` wrapping one of the classes from `twisted.python.logfile`_ as the destination file.

.. _twisted.python.logfile: https://twistedmatrix.com/documents/current/api/twisted.python.logfile.html


``twisted.logger`` integration
------------------------------

If you wish you can direct Eliot logs to Twisted's logging subsystem, if that is the primary logging system you're using.

.. code-block:: python

   from eliot import add_destinations
   from eliot.twisted import TwistedDestination

   add_destinations(TwistedDestination())


Trial Integration
-----------------
If you're using Twisted's ``trial`` program to run your tests you can redirect your Eliot logs to Twisted's logs by calling ``eliot.twisted.redirectLogsForTrial()``.
This function will automatically detect whether or not it is running under ``trial``.
If it is then you will be able to read your Eliot logs in ``_trial_temp/test.log``, where ``trial`` writes out logs by default.
If it is not running under ``trial`` it will not do anything.
In addition calling it multiple times has the same effect as calling it once.

The way you use it is by putting it in your package's ``__init__.py``: it will do the right thing and only redirect if you're using ``trial``.
Take care if you are separately redirecting Twisted logs to Eliot; you should make sure not to call ``redirectLogsForTrial`` in that case so as to prevent infinite loops.


Logging Failures
----------------

``eliot.writeFailure`` is the equivalent of ``eliot.write_traceback``, only for ``Failure`` instances:

.. code-block:: python

    from eliot import writeFailure

    class YourClass(object):

        def run(self):
            d = dosomething()
            d.addErrback(writeFailure)


Actions and inlineCallbacks
---------------------------

Eliot provides a decorator that is compatible with Twisted's ``inlineCallbacks`` but which also behaves well with Eliot's actions.
Simply substitute ``eliot.twisted.inline_callbacks`` for ``twisted.internet.defer.inlineCallbacks`` in your code.

To understand why, consider the following example:

.. code-block:: python

     from eliot import start_action
     from twisted.internet.defer import inlineCallbacks

     @inlineCallbacks  # don't use this in real code, use eliot.twisted.inline_callbacks
     def go():
         with start_action(action_type=u"yourapp:subsystem:frob") as action:
	           d = some_deferred_api()
	           x = yield d
	           action.log(message_type=u"some-report", x=x)

The action started by this generator remains active as ``yield d`` gives up control to the ``inlineCallbacks`` controller.
The next bit of code to run will be considered to be a child of ``action``.
Since that code may be any arbitrary code that happens to get scheduled,
this is certainly wrong.

Additionally,
when the ``inlineCallbacks`` controller resumes the generator,
it will most likely do so with no active action at all.
This means that the log message following the yield will be recorded with no parent action,
also certainly wrong.

These problems are solved by using ``eliot.twisted.inline_callbacks`` instead of ``twisted.internet.defer.inlineCallbacks``.
The behavior of the two decorators is identical except that Eliot's version will preserve the generator's action context and contain it within the generator.
This extends the ``inlineCallbacks`` illusion of "synchronous" code to Eliot actions.

Actions and Deferreds
---------------------

An additional set of APIs is available to help log actions when using Deferreds.
To understand why, consider the following example:

.. code-block:: python

     from eliot import start_action

     def go():
         action = start_action(action_type=u"yourapp:subsystem:frob")
         with action:
             d = Deferred()
             d.addCallback(gotResult, x=1)
             return d

This has two problems.
First, ``gotResult`` is not going to run in the context of the action.
Second, the action finishes once the ``with`` block finishes, i.e. before ``gotResult`` runs.
If we want ``gotResult`` to be run in the context of the action and to delay the action finish we need to do some extra work, and manually wrapping all callbacks would be tedious.

To solve this problem you can use the ``eliot.twisted.DeferredContext`` class.
It grabs the action context when it is first created and provides the same API as ``Deferred`` (``addCallbacks`` and friends), with the difference that added callbacks run in the context of the action.
When all callbacks have been added you can indicate that the action should finish after those callbacks have run by calling ``DeferredContext.addActionFinish``.
As you would expect, if the ``Deferred`` fires with a regular result that will result in success message.
If the ``Deferred`` fires with an errback that will result in failure message.
Finally, you can unwrap the ``DeferredContext`` and access the wrapped ``Deferred`` by accessing its ``result`` attribute.

.. code-block:: python

     from eliot import start_action
     from eliot.twisted import DeferredContext

     def go():
         with start_action(action_type=u"your_type").context() as action:
             d = DeferredContext(Deferred())
             # gotResult(result, x=1) will be called in the context of the action:
             d.addCallback(gotResult, x=1)
             # After gotResult finishes, finish the action:
             d.addActionFinish()
             # Return the underlying Deferred:
             return d.result
