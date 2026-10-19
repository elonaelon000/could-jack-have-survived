"""Build research, story pages and methodological learning notes."""
from build_exhibit import main as build_research
from publish_story import main as publish_story
from document_methods import main as document_methods

if __name__ == '__main__':
    build_research()
    publish_story()
    document_methods()
