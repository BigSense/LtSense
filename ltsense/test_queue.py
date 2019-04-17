#!/usr/bin/env python3
# Author: Sumit Khanna<sumit@penguindreams.org>
# https://bigsense.io
# Copyright 2019
#
# License: GNU GPLv3

import os
import unittest
import tempfile

from ltsense.queue import MemoryQueue, SQLiteQueue


class CommonQueueTests(object):

    def test_enqueue(self):
        self.queue.enqueue('PackageA')
        self.assertEqual(self.queue.size, 1)
        self.queue.enqueue('PackageB')
        self.assertEqual(self.queue.size, 2)
        self.queue.enqueue('PackageC1')
        self.queue.enqueue('PackageC2')
        self.queue.enqueue('PackageC3')
        self.assertEqual(self.queue.size, 5)

    def test_dequeue(self):
        self.queue.enqueue('PackageA')
        self.queue.enqueue('PackageB')
        self.queue.enqueue('PackageC1')
        self.queue.enqueue('PackageC2')
        self.queue.enqueue('PackageC3')
        self.assertEqual(self.queue.dequeue(), 'PackageA')
        self.assertEqual(self.queue.dequeue(), 'PackageB')
        self.assertEqual(self.queue.dequeue(), 'PackageC1')
        self.assertEqual(self.queue.dequeue(), 'PackageC2')
        self.assertEqual(self.queue.dequeue(), 'PackageC3')

    def test_dequeue_empty(self):
        self.assertIsNone(self.queue.dequeue())
        self.queue.enqueue('PackageA')
        self.assertEqual(self.queue.dequeue(), 'PackageA')
        self.assertIsNone(self.queue.dequeue())


class MemoryQueueTest(unittest.TestCase, CommonQueueTests):

    def setUp(self):
        self.queue = MemoryQueue()

    def tearDown(self):
        pass


class SQLiteQueueTest(unittest.TestCase, CommonQueueTests):

    def setUp(self):
        self.sqltemp = tempfile.mkstemp(suffix='.sql')
        self.queue = SQLiteQueue()
        self.queue.data_file = self.sqltemp[1]

    def tearDown(self):
        os.unlink(self.sqltemp[1])