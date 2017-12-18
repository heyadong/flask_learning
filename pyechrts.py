# encoding utf-8

from pyecharts import Bar, Line, Page
from models import Articles

def myecharts():
    time_data = dict()
    page = Page()
    line = Line('博客发布时间分布',title_pos='center',title_color='green',title_top='3%')
    bar = Bar('博客发布时间')
    articles = Articles.query.all()

    for article in articles:
        time = str(article.create_time).split(':')[0]
        if time not in time_data:
            time_data[time] = 1
        else:
            time_data[time] += 1
    line.add('',list(time_data.keys()),list(time_data.values()))
    bar.add('',list(time_data.keys()),list(time_data.values()),is_datazoom_show=True,datazoom_type='both',
             )
    page.add(bar)
    page.add(line)

    return page.render_embed()
