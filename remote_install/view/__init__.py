from flask.views import MethodView
from flask import render_template
from remote_install import app


class BaseApi(MethodView):
    def get_new_template(self):
        raise NotImplementedError()

    def get_objects(self):
        raise NotImplementedError()

    def get_name(self):
        raise NotImplementedError()

    def get_action_name(self):
        raise NotImplementedError()

    def render_new_template(self, form_type, action_type):
        return render_template(self.get_new_template(), form_type=form_type, action_type=action_type)

    def get(self):
        if app.debug:
            app.logger.debug('rendering input form for new %s' % self.get_name())
        return self.render_new_template(form_type=self.get_name(), action_type=self.get_action_name())

    def post(self):
        raise NotImplementedError

