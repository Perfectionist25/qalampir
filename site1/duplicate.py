from django.contrib.auth.models import User
from qalampir.models import News

def duplicate_news(times=10):
    original_news = News.objects.all()
    # Default author tanlaymiz, masalan admin
    default_author = User.objects.first()  # yoki User.objects.get(username='admin')

    count = 0
    for news in original_news:
        for i in range(times):
            News.objects.create(
                title=f"{news.title} (copy {i+1})",
                content=news.content,
                author=default_author
            )
            count += 1
    print(f"{count} new news created!")

