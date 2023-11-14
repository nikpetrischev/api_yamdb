from django.db import models


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='reviews',
    #     verbose_name='Автор отзыва',
    # )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время отзыва',
    )
    # title = models.ForeignKey(
    #     Title,
    #     on_delete=models.CASCADE,
    #     related_name='reviews',
    #     verbose_name='Произведение',
    # )

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "Отзыва"


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='reviews',
    #     verbose_name='Автор комментария',
    # )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время комментария',
    )
    # title = models.ForeignKey(
    #     Title,
    #     on_delete=models.CASCADE,
    #     related_name='comments',
    #     verbose_name='Произведение',
    # )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментария"
