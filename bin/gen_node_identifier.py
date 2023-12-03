#! /usr/bin/env python
"""Derive a unique node identifier."""
import platform
import uuid

print(str(uuid.uuid3(uuid.NAMESPACE_DNS, platform.node())))
