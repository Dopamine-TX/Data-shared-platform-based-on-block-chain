# forms.py
from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, DateField, BooleanField,
                            SelectField, SelectMultipleField, TextAreaField,
                            RadioField, IntegerField, DecimalField, SubmitField,FileField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired

# 定义的表单都需要继承自FlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
	email = StringField(u'邮箱：', validators=[DataRequired(),Email(message=u"邮件格式有误")],render_kw={"placeholder":u"请输入邮箱地址"})
	password = PasswordField(u'密码：', validators=[DataRequired(),Length(max=25)],render_kw={"placeholder":"请输入密码"})
	remember_me = BooleanField('remember me', default=False)
	submit = SubmitField(u'登入')


class RegisterForm(FlaskForm):
	public_key= StringField(u'公钥', validators=[Length(min=60)])
	username = StringField(u'名称', validators=[Length(min=4, max=25)])
	email = StringField('Email Address', validators=[Email()])
	password = PasswordField(u'密码', validators=[Length(min=4, max=25)])
	confirm = PasswordField(u'确认密码',validators=[EqualTo('password', message='Passwords must match')])
	description = TextAreaField(u'介绍')
	submit = SubmitField(u'注册')
	accept_terms = BooleanField('I accept the Terms of Use', default='checked',validators=[DataRequired()])


class DataForm(FlaskForm):
	data_name= StringField(u'数据名称*:',description=u'（例如：2018年**银行的零售客户信息）', validators=[DataRequired(),Length(max=60)])
	detail =  TextAreaField(u'数据详情*:', validators=[DataRequired(),Length(max=200)],render_kw={"placeholder":u"请详细说明贵方数据主要包含哪些信息。例如：人口特征、资产特征、负债特征、结算特征等。200字以内。"})
	beizhu = TextAreaField(u'备注:',  validators=[Length(max=500)],render_kw={"placeholder":u"您可备注相关共享预期以及对共享方的合作要求。例如：我方目的：对零售客户进行聚类细分。合作要求：望数据与我方相似，并且目的统一。500字以内。"})
	submit = SubmitField(u'提交')




class AlgForm(FlaskForm):
	alg_name= StringField(u'算法名称*：',description=u'（例如：基于聚类分析的零售客户细分）', validators=[DataRequired(),Length(max=60)])
	detail =  TextAreaField(u'算法简介*：', validators=[DataRequired(),Length(max=200)],render_kw={"placeholder":u"请简要说明该算法的功能，以及相关技术细节，局限性，适用范围等。200字以内。"})
	data_form = TextAreaField(u'输入数据格式*：',  validators=[DataRequired(),Length(max=500)],render_kw={"placeholder":u"请具体说明该算法的数据输入格式。500字以内。"})
	beizhu = TextAreaField(u'备注：',  validators=[Length(max=500)],render_kw={"placeholder":u"相关注意事项，500字以内。"})
	file = FileField(u"算法源码以及相关附件*：",validators=[FileRequired()])
	submit = SubmitField(u'提交')

#,FileAllowed(['pdf', 'txt'], '只接收.pdf和.txt格式的简历')


#class ShareForm(FlaskForm):
	#self_data =  
	


	
	
    
