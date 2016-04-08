# -*- coding: utf-8 -*-
from datetime import timedelta
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase
from product.models import Product, Comment, Like


class ProductTestCase(TestCase):
    def setUp(self):
        self.user = mixer.blend(User)
        self.user.set_password('123')
        self.user.save()

        self.product = mixer.blend(Product)
        self.actual_comments = mixer.cycle(5).blend(
            Comment, product=self.product)
        self.old_comment = mixer.blend(
            Comment, created_at=timezone.now() - timedelta(hours=24))
        self.likes = []
        for i in xrange(10):
            self.likes.append(mixer.blend(
                Like, product=self.product, user=mixer.blend(User)))

        self.kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def login(self):
        self.client.post(
            reverse('login'),
            {'username': self.user.username, 'password': '123'}
        )

    def product_response(self, slug=None, code=200):
        slug = slug if slug else self.product.slug
        response = self.client.get(
            reverse('product_detail', args=[slug]))
        self.assertEqual(response.status_code, code)
        return response

    def test_is_all_data_showed_on_product_page(self):
        """
        check product data on rendered product page
        """
        response = self.product_response()
        page_params = ['name', 'description']
        for param in page_params:
            self.assertIn(str(getattr(self.product, param)), response.content)

        self.assertIn(
            '<span id="like_for_{0}">{1}</span>'.format(self.product.id, 10),
            response.content
        )

    def test_comments_for_last_24_hours(self):
        """
        check comments on the product page
         it must be only for last 24 hours
        """
        response = self.product_response()
        self.assertItemsEqual(
            response.context['comments'], self.actual_comments)
        self.assertNotIn(
            self.old_comment, response.context['comments'])

    def test_check_product_page_with_bad_slug(self):
        """
        check product page with wrong slug and unicode
        """
        self.product_response('wrong', 404)
        unicode_product = mixer.blend(
            Product, slug=u'слаг', description=u'юникод описание')
        response = self.product_response(unicode_product.slug, 200)
        self.assertIn(
            unicode_product.description, response.content.decode('utf-8'))

    def test_add_like_ajax_for_not_logged_user(self):
        """
        try add like by not logged user
        """
        response = self.client.post(
            reverse('like', args=[self.product.id]), {}, **self.kwargs)
        self.assertRedirects(
            response,
            expected_url='{0}?next={1}'.format(
                reverse('login'), reverse('like', args=[self.product.id])),
            status_code=302,
            fetch_redirect_response=True)

    def test_add_like_ajax_for_logged_user(self):
        """
        make like with logged user
        and make dislike with the same user
        """
        self.login()
        likes = Like.objects.filter(product=self.product).count()

        response = self.client.post(
            reverse('like', args=[self.product.id]), {}, **self.kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            likes+1, Like.objects.filter(product=self.product).count())
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('like', args=[self.product.id]), {}, **self.kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            likes, Like.objects.filter(product=self.product).count())

    def test_get_request_diallowed_for_like(self):
        self.login()
        response = self.client.get(
            reverse('like', args=[self.product.id]))
        self.assertEqual(response.status_code, 405)

    def test_add_comment_by_not_logged_user_with_name(self):
        """
        add comment for ot logged user who entered his name
        """
        comments = Comment.objects.count()
        comment = {
            'name': 'testusername', 'text': 'test comment lalalala'}
        response = self.client.post(
            reverse('product_detail', args=[self.product.slug]), comment)

        self.assertEqual(comments+1, Comment.objects.count())
        self.assertEqual(response.status_code, 200)
        for row in comment.values():
            self.assertIn(row, response.content)

    def test_add_comment_by_not_logged_user_without_name(self):
        """
        add comment for ot logged user who don't entered his name
        """
        comments = Comment.objects.count()
        response = self.product_response()
        self.assertNotIn('Anonym', response.content)
        response = self.client.post(
            reverse('product_detail', args=[self.product.slug]),
            {'text': 'other comment test comment lalalala'})
        self.assertEqual(comments+1, Comment.objects.count())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Anonym', response.content)

    def test_add_comment_by_logged_user(self):
        """
        test make comment with logged user
        """
        self.login()
        comments = Comment.objects.count()
        comment = {'text': 'test comment lalalala'}
        response = self.client.post(
            reverse('product_detail', args=[self.product.slug]), comment)

        self.assertEqual(comments+1, Comment.objects.count())
        self.assertEqual(response.status_code, 200)
        self.assertIn(comment['text'], response.content)
        self.assertIn(self.user.username, response.content)
