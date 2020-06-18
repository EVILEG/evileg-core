# -*- coding: utf-8 -*-

import re

import markdown
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.utils import six
from django.utils.functional import lazy
from django.utils.http import is_safe_url, urlunquote
from django.utils.safestring import mark_safe
from evileg_core.shortcuts import get_object_or_none

mark_safe_lazy = lazy(mark_safe, six.text_type)


class EImageUrlsGetter:
    __slots__ = ['soup']

    def __init__(self, text):
        self.soup = BeautifulSoup(text, "lxml") if text else None

    def handle(self):
        if self.soup:
            src_list = set()
            for tag in self.soup.find_all('img'):
                src_attr = tag.get('src')
                if src_attr and src_attr.startswith('/media/'):
                    src_list.add(src_attr)
            return src_list
        return set()

    @classmethod
    def get_urls(cls, text):
        soup = EImageUrlsGetter(text=text)
        return soup.handle()


class ESoup:
    __slots__ = ['soup', 'tags_for_extracting', 'dofollow', 'add_header_anchors']

    """
    Clean up class for extracting unwanted content from text, which was posted by users
    """
    def __init__(self, text, tags_for_extracting=(), dofollow=False, add_header_anchors=False):
        self.soup = BeautifulSoup(text, "lxml") if text else None
        self.tags_for_extracting = ('script', 'style',) + tags_for_extracting
        self.dofollow = dofollow
        self.add_header_anchors = add_header_anchors

    def _add_header_anchors(self, soup):
        for header_tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            anchor = soup.new_tag('a')
            anchor['class'] = 'anchor'
            anchor['id'] = 'header_{}'.format(header_tag.text.replace(' ', '_'))
            header_tag.insert(0, anchor)
        return soup

    def _extract_tags(self, soup, tags=()):
        for tag in tags:
            for current_tag in soup.find_all(tag):
                current_tag.extract()
        return soup

    def _remove_attrs(self, soup):
        for tag in soup.find_all(True):
            tag.attrs = {}
        return soup

    def _remove_all_attrs_except(self, soup, whitelist_tags=()):
        for tag in soup.find_all(True):
            if tag.name not in whitelist_tags:
                tag.attrs = {}
        return soup

    def _remove_all_attrs_except_saving(self, soup, whitelist_tags=(), whitelist_attrs=(), whitelist_classes=()):
        for tag in soup.find_all(True):
            saved_classes = []
            if tag.has_attr('class'):
                classes = tag['class']
                for class_str in whitelist_classes:
                    if class_str in classes:
                        saved_classes.append(class_str)

            if tag.name not in whitelist_tags:
                tag.attrs = {}
            else:
                attrs = dict(tag.attrs)
                for attr in attrs:
                    if attr not in whitelist_attrs:
                        del tag.attrs[attr]

            if len(saved_classes) > 0:
                tag['class'] = ' '.join(saved_classes)

        return soup

    def _add_rel_attr(self, soup, tag, attr):
        site_url = getattr(settings, "SITE_URL", '/')
        for tag in soup.find_all(tag):
            attr_content = tag.get(attr)
            if attr_content and not attr_content.startswith(site_url) and not attr_content.startswith('/'):
                tag['rel'] = ['nofollow']
        return soup

    def _add_class_attr(self, soup, tag, classes=()):
        for tag in soup.find_all(tag):
            saved_classes = []
            if tag.has_attr('class'):
                saved_classes.append(tag['class'])
            saved_classes.extend(list(classes))
            tag['class'] = ' '.join(saved_classes)
        return soup

    def _add_attr(self, soup, tag, attr, value):
        for tag in soup.find_all(tag):
            tag[attr] = value
        return soup

    def _correct_url(self, soup, tag, attr):
        site_url = getattr(settings, "SITE_URL", None)
        languages = getattr(settings, "LANGUAGES", None)

        if site_url is not None and languages is not None and len(languages) > 1:
            site_url_parser = re.compile('({})'.format('|'.join(['^{}/{}'.format(site_url, code) for code, language in languages])))
            relational_url_parser = re.compile('({})'.format('|'.join(['^/{}'.format(code) for code, language in languages])))

            for tag in soup.find_all(tag):
                attr_content = tag.get(attr)
                if attr_content:
                    attr_content = site_url_parser.sub(site_url, attr_content)
                    attr_content = relational_url_parser.sub('', attr_content)
                    tag[attr] = attr_content

        return soup

    def _change_tag_name(self, soup, old_tag, new_tag):
        for tag in soup.find_all(old_tag):
            tag.name = new_tag
        return soup

    def clean(self):
        if self.soup:
            soup = self._extract_tags(soup=self.soup, tags=self.tags_for_extracting)
            soup = self._remove_all_attrs_except_saving(
                soup=soup,
                whitelist_tags=('img', 'a', 'iframe'),
                whitelist_attrs=('src', 'href', 'name', 'width', 'height', 'alt'),
                whitelist_classes=(
                    'youtube-wrapper', 'youtube-iframe', 'prettyprint', 'lang-bsh', 'lang-c', 'lang-cc', 'lang-cpp',
                    'lang-cs', 'lang-csh', 'lang-cyc', 'lang-cv', 'lang-htm', 'lang-html', 'lang-java', 'lang-js',
                    'lang-m', 'lang-mxml', 'lang-perl', 'lang-pl', 'lang-pm', 'lang-py', 'lang-rb', 'lang-sh',
                    'lang-xhtml', 'lang-xml', 'lang-xsl'
                )
            )
            if not self.dofollow:
                soup = self._add_rel_attr(soup=soup, tag='a', attr='href')
                soup = self._add_rel_attr(soup=soup, tag='img', attr='src')
            soup = self._correct_url(soup=soup, tag='a', attr='href')
            soup = self._correct_url(soup=soup, tag='img', attr='src')
            soup = self._add_attr(soup=soup, tag='img', attr='loading', value='lazy')
            soup = self._add_class_attr(soup=soup, tag='img', classes=('img-fluid',))
            soup = self._add_class_attr(soup=soup, tag='table', classes=('table', 'table-bordered', 'table-hover'))
            soup = self._add_class_attr(soup=soup, tag='code', classes=('prettyprint linenums',))
            soup = self._change_tag_name(soup=soup, old_tag='code', new_tag='pre')
            if self.add_header_anchors:
                soup = self._add_header_anchors(soup=soup)

            return re.sub('<body>|</body>', '', soup.body.prettify())
        return ''

    @classmethod
    def clean_text(cls, text, tags_for_extracting=(), dofollow=False, add_header_anchors=False):
        soup = ESoup(text=text, tags_for_extracting=tags_for_extracting, dofollow=dofollow, add_header_anchors=add_header_anchors)
        return soup.clean()


def set_adding_header_anchors(model, add_header_anchors=True, field_name='content_markdown'):
    model._meta.get_field(field_name).add_header_anchors = add_header_anchors
    for code, language in getattr(settings, "LANGUAGES", []):
        model._meta.get_field('{}_{}'.format(field_name, code)).add_header_anchors = add_header_anchors


class EMarkdownWorker:
    __slots__ = ['pre_markdown_text', 'markdown_text']

    """
    Markdown converter. It will convert markdown text to html text with clean up from unwanted content, using ESoap class
    """
    def __init__(self, text):
        self.pre_markdown_text = text
        self.markdown_text = None
        self.make_html_from_markdown()

    def make_html_from_markdown(self):
        self.markdown_text = markdown.markdown(
            self.pre_markdown_text,
            extensions=['markdown.extensions.attr_list',
                        'markdown.extensions.tables',
                        'markdown.extensions.fenced_code',
                        'markdown.extensions.nl2br',
                        'evileg_core.extensions.video'],
            output_format='html5'
        )

    def get_text(self, dofollow=False, add_header_anchors=False):
        return ESoup.clean_text(text=self.markdown_text, dofollow=dofollow, add_header_anchors=add_header_anchors)


def get_next_url(request):
    """
    Get next url from request. For example it needed for return to previous url.

    :param request: HTTP request
    :return: String
    """
    next = request.META.get('HTTP_REFERER')
    if next:
        next = urlunquote(next)  # HTTP_REFERER may be encoded.
    if not is_safe_url(url=next, allowed_hosts=request.get_host()):
        next = '/'
    return next


def get_client_ip(request):
    """
    Get client ip address from HTTP request

    :param request: HTTP request
    :return: IP Address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[-1].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')


def generate_groups_with_permissions(groups_permissions):
    for group_name in groups_permissions:
        group, created = Group.objects.get_or_create(name=group_name)
        for model_cls in groups_permissions[group_name]:
            for perm_index, perm_name in enumerate(groups_permissions[group_name][model_cls]):
                codename = perm_name + "_" + model_cls._meta.model_name

                permission = get_object_or_none(klass=Permission, codename=codename)
                if permission:
                    group.permissions.add(permission)
