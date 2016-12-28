# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, api


class ReportResultInfo(models.AbstractModel):
    _name = 'report.exam.result_information_report'

    @api.model
    def get_grade(self, result_id, student):
        list_fail = []
        value = {}
        for stu_res in student.year.grade_id.grade_ids:
            value.update({'fail': stu_res.fail})
        list_fail.append(value)
        return list_fail

    @api.model
    def get_lines(self, result_id, student):
        list_result = []
        for sub_id in result_id:
            for sub in sub_id.result_ids:
                std_id = sub_id.standard_id.standard_id.name
                list_result.append({'standard_id': std_id,
                                    'name': sub.subject_id.name,
                                    'code': sub.subject_id.code,
                                    'maximum_marks': sub.maximum_marks,
                                    'minimum_marks': sub.minimum_marks,
                                    'obtain_marks': sub.obtain_marks,
                                    's_exam_ids': sub_id.s_exam_ids.name})
        return list_result

    @api.model
    def get_exam_data(self, result_id, student):
        list_exam = []
        value = {}
        final_total = 0
        count = 0
        per = 0.0
        for res in result_id:
            if res.result_ids:
                count += 1
                per = float(res.total / count)
            final_total = final_total + res.total
            value.update({'result': res.result,
                          'percentage': per,
                          'total': final_total})
        list_exam.append(value)
        return list_exam
    
    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')

        docs = self.env[self.model].browse(self.env.context.get('active_ids',
                                                                []))
        result_id = data['form'].get('result_id')[0]
        student = data['form'].get('student')
        get_grades = self.with_context(data['form'].get('used_context', {}))
        get_grade = get_grades.get_grade(result_id, student)
        get_lines = get_grades.get_lines(result_id, student)
        get_exam_data = get_grades.get_exam_data(result_id, student)
        
        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_grade': get_grade,
            'get_lines': get_lines,
            'get_exam_data': get_exam_data
        }
        render_model = 'exam.result_information_report'
        return self.env['report'].render(render_model, docargs)
