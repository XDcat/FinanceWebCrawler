import docx
from docx.shared import Inches
import os
from config import report_prefix_path
from bs4 import BeautifulSoup



def add_hyperlink(paragraph, url, text, color, underline):
    """
    A function that places a hyperlink within a paragraph object.

    :param paragraph: The paragraph we are adding the hyperlink to.
    :param url: A string containing the required url
    :param text: The text displayed for the url
    :return: The hyperlink object
    """

    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
    hyperlink.set(docx.oxml.shared.qn('r:id'), r_id, )

    # Create a w:r element
    new_run = docx.oxml.shared.OxmlElement('w:r')

    # Create a new w:rPr element
    rPr = docx.oxml.shared.OxmlElement('w:rPr')

    # Add color if it is given
    if not color is None:
      c = docx.oxml.shared.OxmlElement('w:color')
      c.set(docx.oxml.shared.qn('w:val'), color)
      rPr.append(c)

    # Remove underlining if it is requested
    if not underline:
      u = docx.oxml.shared.OxmlElement('w:u')
      u.set(docx.oxml.shared.qn('w:val'), 'none')
      rPr.append(u)

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    paragraph._p.append(hyperlink)

    return hyperlink



class ArticleViewer:

    def __init__(self,article):
        """
        需要article作为参数
        :param article: article数据结构
        """
        self.article=article


    def publish_en_report(self,result_path=None):
        # 传值
        aid = self.article.aid
        website = self.article.website
        kind = self.article.kind
        body = self.article.body
        publish_date = self.article.publish_date
        title = self.article.title
        url = self.article.url
        author = self.article.author
        keyword = self.article.keyword
        attachment = self.article.attachment

        special_char="\\ / : * ? \" \" \' \' < > |".split(" ")
        # 去除title中的特殊字符
        for char in special_char:
            if char in title:
                title=title.replace(char,"")

        if result_path is None:
            result_path_pre= os.path.join(report_prefix_path,"{}-{}/".format(website,kind))
            doc_name ="{}-{}.docx".format(publish_date.replace(" ",""),title)
            if not os.path.exists(result_path_pre):
                os.makedirs(result_path_pre)
            result_path=result_path_pre+doc_name

        # 新建文档对象按模板新建 word 文档文件，具有模板文件的所有格式
        doc = docx.Document()


        # 增加标题:add_heading(self, text="", level=1):
        doc.add_heading(text=title, level=0)

        # 添加作者
        doc.add_paragraph(f'Author:{author}')

        # 添加日期
        doc.add_paragraph(f'Date:{publish_date}')

        # 添加关键词
        if keyword is not None:
            doc.add_paragraph(f'Keyword:{keyword}')
        else:
            doc.add_paragraph(f'Keyword:NA')

        # 添加url
        if url is not None:
            p=doc.add_paragraph("Url:")
            # 在段落中添加文字块，add_run(self, text=None, style=None):返回一个 run 对象
            hyperlink = add_hyperlink(p, url,  'click here', 'FF8822', False)
        else:
            doc.add_paragraph("Url:NA")

        # 添加附件，如果有就写上
        if attachment is not None:
            p=doc.add_paragraph("Attachment:")
            # 在段落中添加文字块，add_run(self, text=None, style=None):返回一个 run 对象
            hyperlink = add_hyperlink(p, attachment,  'click here', 'FF8822', False)
        else:
            doc.add_paragraph("Attachment:NA")

        doc.add_paragraph(f"From:{website}-{kind}")

        # 处理源码字符串，转换为文本
        body = BeautifulSoup(body, "html.parser")
        doc.add_paragraph(text=body.text.strip())

        # 保存文件
        doc.save(result_path)


