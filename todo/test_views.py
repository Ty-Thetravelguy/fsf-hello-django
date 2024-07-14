from django.test import TestCase
from .models import Item


class TestViews(TestCase):

    def test_get_todo_list(self):
        responce = self.client.get('/')
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, 'todo/todo_list.html')

    def test_get_add_item_page(self):
        responce = self.client.get('/add')
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, 'todo/add_item.html')

    def test_get_edit_item_page(self):
        item = Item.objects.create(name='Test Todo Item')
        responce = self.client.get(f'/edit/{item.id}')
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, 'todo/edit_item.html')
        
    def test_can_add_item(self):
        responce = self.client.post('/add', {'name': 'Test Added Item'})
        self.assertRedirects(responce, '/')

    def test_can_delete_item(self):
        item = Item.objects.create(name='Test Todo Item')
        responce = self.client.get(f'/delete/{item.id}')
        self.assertRedirects(responce, '/')
        existing_items = Item.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)

    def test_can_toggle_item(self):
        item = Item.objects.create(name='Test Todo Item', done=True)
        responce = self.client.get(f'/toggle/{item.id}')
        self.assertRedirects(responce, '/')
        updated_item = Item.objects.get(id=item.id)
        self.assertFalse(updated_item.done)

    def test_can_edit_item(self):
        item = Item.objects.create(name='Test Todo Item')
        responce = self.client.post(f'/edit/{item.id}', {'name': 'Updated Name'})
        self.assertRedirects(responce, '/')
        updated_item = Item.objects.get(id=item.id)
        self.assertEqual(updated_item.name, 'Updated Name')