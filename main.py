import configparser
from libs.kanban import Kanban
from pptx import Presentation
from datetime import date, datetime


class PPTBoss():

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.default = config['Default']
        self.kb = Kanban()
        self.prs = None

    def read_from_template(self):
        with open('./ppt/材料組進度報告 - 樣板.pptx', 'rb') as f:
            self.prs = Presentation(f)
            f.close()

    def gen_prs_title_page(self):
        title_slide_layout = self.prs.slide_layouts[2]
        slide = self.prs.slides.add_slide(title_slide_layout)

        title = slide.shapes[1]
        title.text = "材料組進度報告"

        subtitle = slide.shapes[0]
        subtitle.text = f"Rita - {datetime.now().strftime('%Y-%m-%d')}"

    def gen_prs_content_pages(self, project_gid=None):
        for task_id in self.kb.my_tasks.keys():
            content_slide_layout = self.prs.slide_layouts[1]
            slide = self.prs.slides.add_slide(content_slide_layout)

            title = slide.shapes[0]
            title.text = f"{self.kb.my_tasks[task_id]['name']} - {self.kb.my_tasks[task_id]['assignee']['name']}"

            body_shape = slide.placeholders[1]
            tf = body_shape.text_frame
            start_on = self.kb.my_tasks[task_id]['start_on'].strftime("%Y-%m-%d")
            due_on = self.kb.my_tasks[task_id]['due_on'].strftime("%Y-%m-%d")
            is_completed = self.kb.my_tasks[task_id]['completed']
            tf.text = f"任務名稱：{self.kb.my_tasks[task_id]['name']}\n"
            tf.text += f"指派給： {self.kb.my_tasks[task_id]['assignee']['name']}\n"
            tf.text += f"預定時間：{start_on} ~ {due_on}\n"
            if is_completed:
                tf.text += f"狀態：{self.kb.my_tasks[task_id]['completed_at'].strftime('%Y-%m-%d')} 完成"
            elif self.kb.my_tasks[task_id]['start_on'] > date.today():
                tf.text += f"狀態： 尚未開始"
            else:
                tf.text += f"狀態： 進行中..."
            

    def save_file(self, filename=None):
        if filename is None:
            filename = f'./ppt/材料組進度報告_{datetime.today().strftime("%Y%m%d")}.pptx'
        self.prs.save(filename)


if __name__ == '__main__':
    pptboss = PPTBoss()
    pptboss.read_from_template()
    pptboss.gen_prs_title_page()
    pptboss.gen_prs_content_pages()
    pptboss.save_file()
    print('done')