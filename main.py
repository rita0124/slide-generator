from pptx import Presentation
from datetime import datetime


class PPTBoss():

    def __init__(self) -> None:
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

    def save_file(self, filename=None):
        if filename is None:
            filename = f'./ppt/材料組進度報告_{datetime.today().strftime("%Y%m%d")}.pptx'
        self.prs.save(filename)


if __name__ == '__main__':
    pptboss = PPTBoss()
    pptboss.read_from_template()
    pptboss.gen_prs_title_page()
    pptboss.save_file()
    print('done')