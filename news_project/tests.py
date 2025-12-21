from django.test import TestCase, Client
from django.urls import reverse
from .models import News, Category, NewsView


class ViewCountByIPTest(TestCase):
	def setUp(self):
		self.cat = Category.objects.create(name='Test')
		self.news = News.objects.create(title='T', slug='t', body='b', image='images/test.jpg', category=self.cat)
		self.client = Client()

	def test_single_ip_counts_once(self):
		url = reverse('single_page', kwargs={'pk': self.news.pk, 'slug': self.news.slug})
		# first request from IP 1
		resp1 = self.client.get(url, REMOTE_ADDR='1.2.3.4')
		self.news.refresh_from_db()
		self.assertEqual(self.news.views_count, 1)
		self.assertEqual(NewsView.objects.filter(news=self.news, ip_address='1.2.3.4').count(), 1)

		# second request from same IP should not increase the count
		resp2 = self.client.get(url, REMOTE_ADDR='1.2.3.4')
		self.news.refresh_from_db()
		self.assertEqual(self.news.views_count, 1)

	def test_different_ips_increment(self):
		url = reverse('single_page', kwargs={'pk': self.news.pk, 'slug': self.news.slug})
		self.client.get(url, REMOTE_ADDR='1.2.3.4')
		self.client.get(url, REMOTE_ADDR='5.6.7.8')
		self.news.refresh_from_db()
		self.assertEqual(self.news.views_count, 2)
		self.assertEqual(NewsView.objects.filter(news=self.news).count(), 2)
