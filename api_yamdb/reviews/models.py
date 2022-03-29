from django.db import models

class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey( 
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )
