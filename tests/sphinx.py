"""
    sphinx
    ~~~~~~

    Utility functions for testing.  Copied from ``sphinx/testing/util.py``

    :copyright: Copyright 2007-2019 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""


def assert_node(node, cls=None, xpath="", **kwargs):
    if cls:
        if isinstance(cls, list):
            assert_node(node, cls[0], xpath=xpath, **kwargs)
            if cls[1:]:
                if isinstance(cls[1], tuple):
                    assert_node(node, cls[1], xpath=xpath, **kwargs)
                else:
                    assert len(node) == 1, \
                        'The node%s has %d child nodes, not one' % (xpath, len(node))
                    assert_node(node[0], cls[1:], xpath=xpath + "[0]", **kwargs)
        elif isinstance(cls, tuple):
            assert len(node) == len(cls), \
                'The node%s has %d child nodes, not %r' % (xpath, len(node), len(cls))
            for i, nodecls in enumerate(cls):
                path = xpath + "[%d]" % i
                assert_node(node[i], nodecls, xpath=path, **kwargs)
        elif isinstance(cls, str):
            assert node == cls, 'The node %r is not %r: %r' % (xpath, cls, node)
        else:
            assert isinstance(node, cls), \
                'The node%s is not subclass of %r: %r' % (xpath, cls, node)

    for key, value in kwargs.items():
        assert key in node, 'The node%s does not have %r attribute: %r' % (xpath, key, node)
        assert node[key] == value, \
            'The node%s[%s] is not %r: %r' % (xpath, key, value, node[key])
