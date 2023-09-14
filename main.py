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
        subtitle.text = f"大老闆 - {datetime.now().strftime('%Y-%m-%d')}"

    def gen_prs_content_pages(self):
        for team_id, team_name in self.kb.teams.items():
            to_insert = 'N'
            to_insert = input(f'加入組別: {team_name} ?(Y或y新增)')
            if to_insert in 'Yy':
                self.kb.get_users_in_team(team_id)
                self.kb.get_projects_in_team(team_id)
                for project_id, project_name in self.kb.projects.items():
                    to_insert = 'Y'
                    # to_insert = input(f'加入專案: {project_name} ?(Y?)')
                    if to_insert in 'Yy':
                        # self.kb.get_tasks_in_project(project_id)
                        for user in self.kb.users.keys():
                            self.kb.get_tasks_in_project_details(assignee_gid=user, project_gid=project_id)
                            self.kb.clean_empty_values_in_my_tasks()
                            for task_id in self.kb.my_tasks.keys():
                                print(f"{self.kb.my_tasks[task_id]}")
                                if self.kb.my_tasks[task_id]['name'] == '無名氏':
                                    break
                                content_slide_layout = self.prs.slide_layouts[1]
                                slide = self.prs.slides.add_slide(content_slide_layout)

                                title = slide.shapes[0]
                                title.text = f"{self.kb.my_tasks[task_id]['name']} - {self.kb.my_tasks[task_id]['assignee']['name']}"

                                body_shape = slide.placeholders[1]
                                tf = body_shape.text_frame
                                if 'start_on' not in self.kb.my_tasks[task_id].keys():
                                    continue
                                if 'due_on' not in self.kb.my_tasks[task_id].keys():
                                    continue
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
                    else:
                        print(f'略過專案: {project_name}')
                        continue
            else:
                print(f'略過組別: {team_name}')
                continue

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