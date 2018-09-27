

class Pagination:
    def __init__(self,current_page,count,per_page_size,pagination_size=11):
        self.current_page = current_page
        self.count = count
        self.per_page_size = per_page_size
        self.pagination_size = pagination_size

    @property
    def db_start(self):
        return (self.current_page - 1) * self.per_page_size

    @property
    def db_end(self):
        return self.current_page * self.per_page_size

    def get_page_html(self):
        cls_item_count,remainer = divmod(self.count, self.per_page_size)
        half_pagination_size,remainer = divmod(self.pagination_size, 2)
        pagination_html_list = []
        if self.count < self.pagination_size:
            pagination_start = 1
            pagination_end = cls_item_count
        else:
            if self.current_page - half_pagination_size <= 0:
                pagination_start = 1
                pagination_end = self.pagination_size
            elif self.current_page + half_pagination_size > cls_item_count:
                pagination_start = cls_item_count - 10 + 1
                pagination_end = cls_item_count + 1
            else:
                pagination_start = self.current_page - half_pagination_size
                pagination_end = self.current_page + half_pagination_size
        if self.current_page == 1:
            pagination_html_list.append("<a href='#'>上一页</a>")
        else:
            prev_pagination = self.current_page - 1
            pagination_html_list.append("<a href='/manager/classes?p=%s'>上一页</a>" % prev_pagination)
        for i in range(pagination_start, pagination_end + 1):
            pagination_html_list.append("<a href='/manager/classes?p=%s'>%s</a>" % (i, i))
        if self.current_page - 1 == cls_item_count:

            pagination_html_list.append("<a href='#'>下一页</a>")
        else:
            next_pagination = self.current_page + 1
            pagination_html_list.append("<a href='/manager/classes?p=%s'>下一页</a>" % next_pagination)
        pagination_html_str = "".join(pagination_html_list)
        return pagination_html_str