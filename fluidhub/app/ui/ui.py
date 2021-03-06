
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import glob, os
import hashlib

from flask import Blueprint,render_template,url_for,redirect,session,g,flash,abort
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField

from FluidHub.ConfigManager import ConfigMan
from FluidHub.UsersManager import UsersMan
from FluidHub.TokenManager import TokenManager
from FluidHub import Constants

import uiCommon
import uiHome
import uiAdmin
import uiWareshub


################################################################################
################################################################################


class LoginForm(FlaskForm):
    Username = StringField('Username')
    Password = PasswordField('Password')
    Signin = SubmitField("Sign in")
    Signout = SubmitField("Sign out")
    #Remember = BooleanField('Remember me for 14 days') # TODO Implement remember login


################################################################################
################################################################################


ui = Blueprint('ui',__name__,
               template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates"),
               static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),"static"))


################################################################################
################################################################################


@ui.before_request
def CheckCredentials():

  g.IsAdmin = False
  g.LoginF = LoginForm()

  if g.LoginF.validate_on_submit() :
    if  g.LoginF.Signin.data :
      # Manage signin submit
      if UsersMan.authenticateUser(g.LoginF.Username.data,g.LoginF.Password.data) :
        session["usertoken"] = TokenManager.generate(g.LoginF.Username.data,ConfigMan.getint("ui","tokenexp"))
        session["username"] = g.LoginF.Username.data
        Code,Infos = UsersMan.getUser(g.LoginF.Username.data)
        session["fullname"] = Infos["fullname"]
        session["email"] = Infos["email"]
        session["gravatarid"] = hashlib.md5(Infos["email"].lower()).hexdigest()
        if not len(session["fullname"]):
          session["fullname"] = session["username"]
      else:
        flash("invalid login")
    elif g.LoginF.Signout.data :
      # Manage signout submit
      session.pop('username', None)
      session.pop('fullname', None)
      session.pop('usertoken', None)
      session.pop('email', None)
      session.pop('gravatarid', None)

  # check token validity
  if "usertoken" in session and not TokenManager.decode(session["usertoken"]) :
    flash("invalid or expired credentials")
    session.pop('username', None)
    session.pop('fullname', None)
    session.pop('usertoken', None)
    session.pop('email', None)
    session.pop('gravatarid', None)

  if "usertoken" in session and "username" in session and UsersMan.isAdmin(session["username"]) :
    g.IsAdmin = True


################################################################################


@ui.errorhandler(404)
def Manage404(e):
  Vars = uiCommon.initTemplateVariables()
  return render_template('404.html',**Vars), 404


################################################################################


@ui.errorhandler(500)
def Manage500(e):
  Vars = uiCommon.initTemplateVariables()
  return render_template('500.html',**Vars), 500


################################################################################


@ui.route("/",methods=['GET','POST'])
def Home():
  return uiHome.render()


################################################################################


@ui.route("/admin",methods=['GET','POST'])
def AdminHome():
  if not g.IsAdmin:
    return redirect(url_for(".Home"))

  return uiAdmin.renderAdminHome()


################################################################################


@ui.route("/admin/users",methods=['GET','POST'])
def AdminUsersList():
  if not g.IsAdmin:
    return redirect(url_for(".Home"))

  return uiAdmin.renderAdminUsersList()


################################################################################


@ui.route("/admin/users/<username>",methods=['GET','POST'])
def AdminUserDetails(username):
  if not g.IsAdmin:
    return redirect(url_for(".Home"))

  return uiAdmin.renderAdminUserDetails(username)


################################################################################


@ui.route("/wareshub",methods=['GET','POST'])
def WaresHome():
  return uiWareshub.renderWaresHome()


################################################################################


@ui.route("/wareshub/<string:ware_type>",methods=['GET','POST'])
def WaresList(ware_type):
  return uiWareshub.renderWaresList(ware_type)


################################################################################


@ui.route("/wareshub/<string:ware_type>/<string:ware_id>",methods=['GET','POST'])
def WareDetails(ware_type,ware_id):
  return uiWareshub.renderWareDetails(ware_type,ware_id)


################################################################################


@ui.route("/wareshub/<string:ware_type>/<string:ware_id>/pdf",methods=['GET'])
def WarePDFDoc(ware_type,ware_id):
  return uiWareshub.renderWarePDFDoc(ware_type,ware_id)
