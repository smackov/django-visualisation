# The "Visualization" site

Visualization - the site for tracking your productivity. It's a good tool to visual your work time.
Beneath you can see screen from index page of the site. It's dashboard showing your information about your work.

![Index page](./readme_assets/index_page.png)

#### Reference to the site: [www.smackov.ru](http://www.smackov.ru/)
## Technologies used:

* ___Backend___: Python 3.8 / Django 3.x
* ___Frontend___: Bootstrap 4.5
* ___System___: nginx 1.8 / Gunicorn / Supervisor / Ubuntu Server
* ___Server host___: Digital Ocean
* ___Database___: PostgreSQL

## Description

This site is designed to record and visualize completed tasks. You can create a task like `English`. As you work on a task and allocate time for it, you can record the time spent in your own profile to see how much time you spend on a given task, and when you did it. After working on the task for 1 hour _(or 2 tomatoes for 25-30 minutes)_, you create a `track`, which says that on a certain day you were engaged in a certain task for a certain amount of time with a certain result (`rate`).

## Dashboard at index page

The dashboard can show you how many time you have spent for work. Beneath you can sea part of this board:

![Statistic on the dashboard](./readme_assets/dashboard_statistic.png)

This paned contains 3 parts:
* _Week status_ - it shows how many time we have been working in current week. At this example we have 11 hours of 30 hours that we planned to work.
* _Last 4 weeks_ - it shows how many time we worked in last 4 week, excluding current week. It's a good overview to look our past efforts.
* _Statistic_ - it's more general representation of our work. At this point statistic shows how many hours we spent for work in the current month, last month or at all.
