from django.test import TestCase
from django.urls import reverse

from apps.books.models import Book, BookReview
from apps.users.models import User
from django.test import Client
from django.contrib.messages.storage.fallback import FallbackStorage



class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:book-list"))
        self.assertContains(response, "No Books")
        self.assertEquals(response.status_code, 200)

    def test_book_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", slug="book1", published="2000-12-12",
                                    isbn="218983981", page=123)
        book2 = Book.objects.create(title="Book2", description="Description2", slug="book2", published="2000-12-12",
                                    isbn="218983911", page=123)

        response = self.client.get(reverse("books:book-list"))
        self.assertContains(response, book1.title)
        self.assertContains(response, book1.description)
        self.assertContains(response, book2.title)
        self.assertContains(response, book2.description)
        self.assertEquals(response.status_code, 200)

    def test_book_detail(self):
        book1 = Book.objects.create(title="Book1", description="Description1", slug="book1", published="2000-12-12",
                                    isbn="218983981", page=123)
        user = User.objects.create(
            username="test",
            middle_name="Test1"
        )
        user.set_password("testpass")
        user.save()
        review = BookReview.objects.create(
            user=user,
            book=book1,
            body="Body1",
            rating=5
        )
        response = self.client.get(reverse("books:book-detail", kwargs={"slug": book1.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, book1.title)
        self.assertContains(response, book1.description)
        self.assertContains(response, book1.page)
        self.assertContains(response, book1.isbn)
        self.assertContains(response, 12)
        self.assertContains(response, 2000)
        self.assertContains(response, "Dec")
        self.assertContains(response, review.rating)
        self.assertContains(response, review.user.username)
        self.assertContains(response, review.body)



class AddReviewViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
    
    def test_add_review_valid_form(self):
        book = Book.objects.create(title='Test Book', author='Test Author')
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('books:add-review', kwargs={'pk': book.id}), {
            'body': 'Test review body',
            'rating': 5
        })
        
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(BookReview.objects.filter(book=book, user=self.user).count(), 1)  
        
    def test_add_review_invalid_form(self):
        book = Book.objects.create(title='Test Book', author='Test Author')
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('books:add-review', kwargs={'pk': book.id}), {
            'body': '',  
            'rating': 5
        })
        
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(BookReview.objects.filter(book=book, user=self.user).count(), 0)  



    def test_review_delete(self):
        review = BookReview.objects.create(user=self.user, book=Book.objects.create(title='Test Book'), body='Test body', rating=5)
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('books:review-delete', kwargs={'pk': review.id}))
        
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(BookReview.objects.filter(pk=review.id).exists())  
        
    def test_review_update(self):
        review = BookReview.objects.create(user=self.user, book=Book.objects.create(title='Test Book'), body='Test body', rating=5)
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('books:review-update', kwargs={'pk': review.id}), {
            'body': 'Updated body',
            'rating': 4
        })
        
        self.assertEqual(response.status_code, 302)  
        updated_review = BookReview.objects.get(pk=review.id)
        self.assertEqual(updated_review.body, 'Updated body')  
        self.assertEqual(updated_review.rating, 4)  