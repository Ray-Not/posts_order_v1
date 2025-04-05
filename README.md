Команды в shell
1.	py manage.startapp newapp
2.	py manage.py shell
3.	py manage.py makemigrations
4.	py manage.py migrate
5.	>>> from newapp.models import *
6.	>>> user1 = User.objects.create(username='Mike', first_name='Frank') 
7.	>>>Author.objects.create(authorUser=user1)
8.	>>>Category.objects.create(authorUser=user2)
9.	User2 = User.objects.create(username='Semyon',  first_name='Ber')
10.	Author.objects.create(authorUser=user2)
11.	Category.objects.create(name='IT')
12.	Category.objects.create(name='Education')
13.	Post.objects.create(author=Author.objects.get(AuthorUser=User.objects.get(username="Mike")), CategoryType="NW", title="title", text="some text")
14.	p1 = Post.objects.get(pk=1)  
15.	c1 = Category.objects.get(name="IT")
16.	p1.postCategory.add(c1)
17.	Comment.objects.create(commentUser=User.objects.get(username="Mike"), commentPost= Post.objects.get(pk=1), text="comment text1")
18.	Post.objects.get(pk=1).like()
19.	Comment.objects.get(pk=1).like()
20.	Author.objects.get(AuthorUser=User.objects.get(username='Mike')).update_rating()
21.	a=Author.objects.get(AuthorUser=User. objects.get(username='Semyon'))
22.	a.ratingAuthor
23.	Author.objects.get(AuthorUser=User. objects.get(username='Mike')).ratingAuthor
24.	best = Author.objects.all().order_by("-ratingAuthor").values("authorUser","ratingAuthor")[0]
25.	print(best)
