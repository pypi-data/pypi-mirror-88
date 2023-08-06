import time
from enum import Enum

import numpy as np
from graphviz import Digraph

from pyautodiff import Mode


class NodeType(Enum):
    var = 0
    const = 1
    operation = 2


class Viser(object):
    """
    A class to draw the computational graph and auto diff trace by graphviz.Digraph (directed graph).
    To distinguish the computational graph and the AD trace, two families of arrow will be used:
    1. For the computational graph, use full arrow. Black one represents the first operand, while one represents the
    second operand.
    2. For the AD trace, use half arrow. Black one represents the Forward mode and the white for the reverse/mix mode.
    If the arrow has the upper part, it indicates the var is the first operand; the lower part indicates the second
    operand.
    To use:
    Viser(Var(1, 'x') + Var(2, 'y'), draw_AD_trace=False)
    """

    def __init__(self, x, draw_AD_trace=False, horizontal=True):
        """

        Args:
            x: a Var instance containing the operation result
            draw_AD_trace: defaults to False, plot the computational graph. If True, draw the AD trace
            horizontal: defaults to True, extend the plot horizontally (lfet->right); If False, draw the plot ,
            vertically (top->down).
        """
        self.n_nodes = 1
        self.ad_trace = draw_AD_trace

        self.g = Digraph('Trace', format='png')
        if horizontal:
            self.g.attr(rankdir='LR')

        self.g.node("0", label="output")
        self._draw(x, "0")

    @staticmethod
    def _get_op_symbol(cls):
        """
        Return the symbol of operation to display on the plot. For example, symbol of VarAdd: "+".
        Args:
            cls: Operation class

        Returns:

        """
        if cls.symbol is None:
            return cls.__name__[3:]
        return cls.symbol

    def _get_unique_id(self):
        """
        Generate a unique id for node.
        Returns:
            a string for id
        """
        return f"{time.process_time()}_{self.n_nodes}"

    @staticmethod
    def _get_color(xtype):
        """
        Return the color for node by node(var) type.
        Args:
            xtype: node type

        Returns:
            a string for color
        """
        return {
            NodeType.var: None,
            NodeType.const: "darkseagreen2",
            NodeType.operation: "lavender",
        }[xtype]

    @staticmethod
    def _get_shape(xtype):
        """
        Return the shape for node by node(var) type.
        Args:
            xtype: node type

        Returns:
            a string for shape
        """
        return {
            NodeType.var: "oval",
            NodeType.const: "oval",
            NodeType.operation: "box",
        }[xtype]

    @staticmethod
    def _get_style(xtype):
        """
        Return the box style for node by node(var) type.
        Args:
            xtype: node type

        Returns:
            a string for box style
        """

        return {
            NodeType.var: None,
            NodeType.const: "filled",
            NodeType.operation: "filled",
        }[xtype]

    @staticmethod
    def _get_arrow(is_second_operand=False, ad=False, reverse_mode=False):
        """
        Return the arrow type for node by node(var) type. The arrow type see the docstring of class.
        Args:
            xtype: node type

        Returns:
            a string for arrow type
        """

        if ad:
            if reverse_mode:
                return "ornormal" if is_second_operand else "olnormal"

            return "rnormal" if is_second_operand else "lnormal"

        return "onormal" if is_second_operand else "normal"

    @staticmethod
    def _beatify_val(val):
        """Keep at most 3 digits for float"""
        return np.around(val, 3)

    def _draw(self, x, father, is_second_operand=False):
        """
        Draw the graph recursivley. The graph stores in self.g.
        Be careful, the direction of the arrow is determined by the propagation direction.
        Args:
            x: a var instance, a member of a composite operation
            father: x's "previous" node.
            is_second_operand: True/False

        Returns:
            None
        """
        try:
            cls, operands = x._context
            xid = self._get_unique_id()
            xlabel = self._get_op_symbol(cls)
            xtype = NodeType.operation
        except:
            operands = []

            if x.name is None:
                xid = self._get_unique_id()
                xlabel = f"{self._beatify_val(x.val)}"
                xtype = NodeType.const
            else:
                xid = xlabel = x.name
                xtype = NodeType.var

        self.g.node(xid, label=xlabel,
                    color=self._get_color(xtype),
                    shape=self._get_shape(xtype),
                    style=self._get_style(xtype))

        if father is not None:
            if self.ad_trace and x.mode != Mode.Forward:
                self.g.edge(father, xid, arrowhead=self._get_arrow(is_second_operand, True, True))
            else:
                self.g.edge(xid, father, arrowhead=self._get_arrow(is_second_operand, self.ad_trace, False))

        for i, t in enumerate(operands):
            self._draw(t, xid, i == 1)

    def show(self):
        """Show the plot. For IPython/jupyter notebook, call "self.g" directly"""
        self.g.view(cleanup=True, directory="/tmp")

    def save(self, path):
        """Pass in a string as path, save the plot to local"""
        self.g.render(path)
