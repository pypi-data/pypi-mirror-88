from html.parser import HTMLParser
from typing import List, Optional

from .exceptions import WrongHTMLFormatError
from .node import Node, Nodes


def parse(html: str, show_unclosed_tags: bool = True, strict_parsing: bool = True,
          auto_close: List[str] = None) -> Nodes:
    """
    Main functions to parse html source. Returns Nodes object back to use it with queries
    :param html: string html-content
    :param show_unclosed_tags: flag to show all unclosed tags on parsing error. If strict_parsing is False, then will
    be ignored
    :param strict_parsing: flag to check markup (closing tag must be for same opened tag etc.) if False then nothing
    checks and all relative-style query will return None or Error
    :param auto_close: list of tags for auto-closing when parse, can be used to fix markup issues
    :return: Nodes object
    :raises WrongHTMLFormatError if wrong format and strict_parsing is True
    """
    parser = MyHTMLParser(auto_close) if strict_parsing else RelaxedHTMLParser()
    # TODO fix it
    Node.comments.clear()
    parser.feed(html)
    if strict_parsing:
        if show_unclosed_tags and parser.unclosed_nodes:
            message = "\nUNCLOSED TAGS:\n" + "\n".join(e.__repr__() for e in parser.unclosed_nodes)
            print(message)
        unclosed_at_all = [e for e in parser.all_nodes._flatten() if not e.closed]
        if unclosed_at_all:
            message = "\nThese tags was not closed (even by its parent):\n" + \
                      "\n".join(e.__repr__() for e in unclosed_at_all)
            print(message)
            raise WrongHTMLFormatError(f'Some tags was not closed itself or by parents, count= {len(unclosed_at_all)}')
    return parser.all_nodes


class MyHTMLParser(HTMLParser):
    VOID = ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
            'meta', 'param', 'source', 'track', 'wbr')

    def __init__(self, auto_close: List = None):
        super().__init__()
        if auto_close:
            MyHTMLParser.VOID += tuple(auto_close)
        self.actual_node: Optional[Node] = None
        self.all_nodes: Nodes = Nodes()
        self.unclosed_nodes = Nodes()

    def handle_starttag(self, tag, attrs):
        attrs = None if not attrs else attrs
        if self.actual_node is None:
            self.actual_node = Node(tag=tag, attrs=attrs)
            self.all_nodes.append(self.actual_node)
        else:
            node = Node(tag, attrs=attrs)
            node._parent = self.actual_node
            if self.actual_node.has_child():
                self.actual_node._children[-1]._next_node = node
                node._prev_node = self.actual_node._children[-1]
            self.actual_node._children.append(node)
            self.actual_node = node
        if tag in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str):
        if self.actual_node is None:
            raise WrongHTMLFormatError(f'Closed tag ({tag}) without opening!')
        self.actual_node.closed = True
        if self.actual_node.tag == tag:
            self.actual_node.closed = True
            if self.actual_node.has_parent():
                self.actual_node = self.actual_node.parent
            else:
                self.actual_node = None
        else:
            self.unclosed_nodes.append(self.actual_node)
            self._find_opened_tag(tag, self.actual_node)

    def _find_opened_tag(self, tag: str, actual_node: Node):
        while actual_node.has_parent():
            actual_node = actual_node.parent
            actual_node.closed = True
            if actual_node.tag == tag:
                if actual_node.has_parent():
                    self.actual_node = actual_node.parent
                else:
                    self.actual_node = None
                return
            else:
                self.unclosed_nodes.append(actual_node)
        raise WrongHTMLFormatError(f'Cant find open tag for closed tag "{tag}"')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self.actual_node is not None:
            self.actual_node._set_text(data)

    def handle_comment(self, data):
        Node.comments.append(data)

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

    def handle_decl(self, data):
        pass

    def error(self, message):
        raise WrongHTMLFormatError('Parser error!\n' + message)


class RelaxedHTMLParser(HTMLParser):
    """
    Parser realisation which ignores markup failures, just collects all html-elements
    WARNING! You cant use any relative-type queries with current parser! All next, previous, children, parent for all
    nodes is None
    """

    def __init__(self):
        super().__init__()
        self.actual_node = None
        self.all_nodes = Nodes()

    def handle_starttag(self, tag, attrs):
        attrs = None if not attrs else attrs
        self.actual_node = Node(tag=tag, attrs=attrs)
        self.all_nodes.append(self.actual_node)

    def handle_endtag(self, tag):
        pass

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if self.actual_node is not None:
            self.actual_node._set_text(data)

    def handle_comment(self, data):
        Node.comments.append(data)

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

    def handle_decl(self, data):
        pass

    def error(self, message):
        raise WrongHTMLFormatError('Parser error!\n' + message)
