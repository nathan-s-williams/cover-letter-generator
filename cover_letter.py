import os
import re
import shutil
import string
from datetime import datetime
from docx import Document


class CoverLetter:
    # ********************************************************************
    # --Static Class Variables
    # ********************************************************************
    _web_template_source = "./cover_letter_templates/cover_letter_template_web.txt"
    _template_destination = "./cover_letter_temp_files/"

    VERSION_TYPE_WEB = "web"  # Change to unique object for validation
    VERSION_TYPE_NEW = "new"

    def __init__(self):
        # Attributes
        self._version = None
        self._date = None
        self._cover_letter = None
        self._company = None
        self._role = None
        self._cover_letter_content = None
        self._template_populated = False

    # ********************************************************************
    # --Setters
    # ********************************************************************
    def set_company(self, company_name: string):
        self._company = company_name
        if self._template_populated:
            self._template_populated = False

    def set_job_role(self, job_name: string):
        self._role = job_name
        if self._template_populated:
            self._template_populated = False

    def set_date(self, date: string):
        self._date = date
        if self._template_populated:
            self._template_populated = False

    def set_version(self, version: string):
        self._version = version
        if self._template_populated:
            self._template_populated = False
        self._create_template()

    def set_cover_letter_content(self, content: string):
        self._cover_letter_content = content

    # ********************************************************************
    # --Getters
    # ********************************************************************
    def get_company(self):
        return self._company

    def get_job_role(self):
        return self._role

    def get_date(self):
        return self._date

    def get_version(self):
        return self._version

    def get_cover_letter_content(self):
        return self._cover_letter_content

    # ********************************************************************
    # --Class Methods
    # ********************************************************************
    def _create_template(self):
        # **************************
        # Create web template
        # **************************
        if self._version is CoverLetter.VERSION_TYPE_WEB:  # object equality
            self._cover_letter = (CoverLetter._template_destination + self._version +
                                  "_cover_letter " + str(datetime.now()))
            shutil.copy(CoverLetter._web_template_source, self._cover_letter)

            # Read content to cover_letter_content class variable
            with open(self._cover_letter, "r") as f:
                self._cover_letter_content = f.read()
        else:
            raise Exception("Version not defined.")

    def insert_data(self):
        # **************************
        # Check data
        # **************************
        if self._date is None or self._role is None or self._company is None or self._version is None:
            list_of_missing_data = []
            if self._version is None:
                list_of_missing_data.append("Version")
            if self._date is None:
                list_of_missing_data.append("Date")
            if self._role is None:
                list_of_missing_data.append("Role")
            if self._company is None:
                list_of_missing_data.append("Company")

            missing_data = ""
            while len(list_of_missing_data) > 0:
                if len(list_of_missing_data) == 1:
                    missing_data += list_of_missing_data.pop()
                else:
                    missing_data += list_of_missing_data.pop() + ", "
            raise Exception(missing_data + " is missing.")

        # **************************
        # Insert Data
        # **************************

        self._cover_letter_content = re.sub("___DATE___", self._date, self._cover_letter_content)
        self._cover_letter_content = re.sub("___JOBTITLE___", self._role, self._cover_letter_content)
        self._cover_letter_content = re.sub("___COMPANYNAME___", self._company, self._cover_letter_content)

        # **************************
        # Write Content
        # **************************

        with open(self._cover_letter, "w") as f:
            f.write(self._cover_letter_content)

        # **************************
        # Checkpoint: template populated
        # **************************
        self._template_populated = True

    def generate_word_doc(self, file_destination: string = "./cover_letter_outputs"):
        if not self._template_populated:
            raise Exception("Template has not been created yet.")

        document = Document()
        document.add_paragraph(self._cover_letter_content)
        document.save(os.path.join(file_destination, "Cover_Letter_Nathan_Williams.docx"))

    def generate_text_doc(self, file_destination: string = "./cover_letter_outputs"):
        if not self._template_populated:
            raise Exception("Template has not been created yet.")
        shutil.copy(self._cover_letter, os.path.join(file_destination, "Cover_Letter_Nathan_Williams.txt"))

    @staticmethod
    def clean_up():
        # clean up temp files and any other artifacts
        for file in os.listdir(CoverLetter._template_destination):
            if file[0] == ".":
                continue
            os.remove(os.path.join(CoverLetter._template_destination, file))
