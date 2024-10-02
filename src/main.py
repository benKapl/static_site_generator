from textnode import TextNode, TextType
import sys


def main():
    dummy_textnode = TextNode("Deux bibous sont amoureux", TextType.BOLD, "https://www.bibous4ever.com")
    print(dummy_textnode)
    return dummy_textnode

if __name__ == "__main__":
    main()

    p = sys.path
    print(p)

