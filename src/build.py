"""Build the research deliverables and both entry points of the story-first site."""
from build_exhibit import main as build_research
from publish_story import main as publish_story

if __name__ == '__main__':
    build_research()
    publish_story()
