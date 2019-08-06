# -*- coding: utf-8 -*-

import markdown
from markdown.util import etree


class VideoExtension(markdown.Extension):

    def add_inline(self, md, name, klass, re):
        pattern = klass(re)
        pattern.md = md
        pattern.ext = self
        md.inlinePatterns.add(name, pattern, "<reference")

    def extendMarkdown(self, md, md_globals):
        self.add_inline(md, 'dailymotion', Dailymotion,
                        r'([^(]|^)https?://www\.dailymotion\.com/video/(?P<dailymotionid>[a-zA-Z0-9]+)(_[\w\-]*)?')
        self.add_inline(md, 'metacafe', Metacafe,
                        r'([^(]|^)https://www\.metacafe\.com/watch/(?P<metacafeid>\d+)/?(:?.+/?)')
        self.add_inline(md, 'vimeo', Vimeo,
                        r'([^(]|^)https://(www.|)vimeo\.com/(?P<vimeoid>\d+)\S*')
        self.add_inline(md, 'youtube', Youtube,
                        r'([^(]|^)https?://www\.youtube\.com/watch\?\S*v=(?P<youtubeid>\S[^&/]+)')
        self.add_inline(md, 'youtube_short', Youtube,
                        r'([^(]|^)https?://youtu\.be/(?P<youtubeid>\S[^?&/]+)?')


class Dailymotion(markdown.inlinepatterns.Pattern):

    def handleMatch(self, m):
        return render_video('//www.dailymotion.com/embed/video/{}'.format(m.group('dailymotionid')))


class Metacafe(markdown.inlinepatterns.Pattern):

    def handleMatch(self, m):
        return render_video('//www.metacafe.com/embed/{}/'.format(m.group('metacafeid')))


class Vimeo(markdown.inlinepatterns.Pattern):

    def handleMatch(self, m):
        return render_video('//player.vimeo.com/video/{}'.format(m.group('vimeoid')))


class Youtube(markdown.inlinepatterns.Pattern):

    def handleMatch(self, m):
        return render_video('//www.youtube.com/embed/{}'.format(m.group('youtubeid')))


def render_video(url):
    iframe = etree.Element('iframe')
    iframe.set('src', url)
    iframe.set('allowfullscreen', 'true')
    iframe.set('frameborder', '0')
    iframe.set('class', 'youtube-iframe')
    div = etree.Element('div')
    div.set('class', 'youtube-wrapper pb-3 border-0')
    div.append(iframe)
    return div


def makeExtension(**kwargs):
    return VideoExtension(**kwargs)
