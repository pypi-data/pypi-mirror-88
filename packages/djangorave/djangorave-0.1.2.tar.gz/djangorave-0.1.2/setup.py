# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangorave',
 'djangorave.migrations',
 'djangorave.templatetags',
 'djangorave.tests']

package_data = \
{'': ['*'], 'djangorave': ['static/djangorave/js/*', 'templates/djangorave/*']}

install_requires = \
['django>=2.2,<4', 'djangorestframework>=3.10,<4.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'djangorave',
    'version': '0.1.2',
    'description': 'Django integration for Flutterwave Rave Card payments and subscriptions',
    'long_description': '# Django Rave\n\n## Project Description\n\nThis project provides Django integration for [Flutterwave](https://flutterwave.com/) Rave Card payments and subscriptions.\n\nCurrent functionality:\n- Allow users to make payments (once off and subscription)\n- Create payment buttons which launch Rave payment modals\n- Maintain a transaction history linked to users\n\n# Requirements\n\n- Python >= 3.6\n- Django >= 2.0\n\n# Installation\n\n```bash\npip install djangorave\n```\n\n# Setup\n\nAdd `"djangorave"` to your `INSTALLED_APPS`\n\nRun Django migrations:\n\n```python\nmanage.py migrate\n```\n\nAdd the following to your `settings.py`:\n\n```python\nRAVE_PRODUCTION_PUBLIC_KEY = "your key"\nRAVE_PRODUCTION_SECRET_KEY = "your key"\nRAVE_SANDBOX_PUBLIC_KEY = "your key"\nRAVE_SANDBOX_SECRET_KEY = "your key"\nRAVE_SANDBOX = True\n```\n\nThe above config will ensure `djangorave` uses your Rave sandbox. Once you are\nready to go live, set `RAVE_SANDBOX = False`\n\nAdd `djangorave` to your `urls.py`:\n\n```python\npath("djangorave/", include("djangorave.urls", namespace="djangorave"))\n```\n\nAdd the following url as a webhook in your Rave dashboard. This will be used by\nRave to `POST` payment transactions to your site:\n\n```bash\nhttp://yoursite.com/djangorave/transaction/\n```\n\n`Note:` while in development, a tool like ngrok (or similar) may prove useful.\n\n# Usage\n\n`djangorave` provides two models, namely:\n\n- The `DRPaymentTypeModel` allows you to create `once off` or `recurring` payment types. When creating a `recurring` payment type, ensure the `payment_plan` field\ncorresponds to the Rave `Plan ID`.\n- The `DRTransactionModel` creates transactions when Rave POSTS to the above mentioned webhook url. This provides a history of all transactions (once off or recurring), linked to the relevant `DRPaymentTypeModel` and `user`.\n\nA payment button can be created as follows:\n\n1. Create a new `PaymentType` using the django admin.\n2. In the view where you wish the button to appear, add the above created `PaymentType` to your context, eg:\n\n```python\nfrom djangorave.models import DRPaymentTypeModel\n\nclass SignUpView(TemplateView):\n    """Sign Up view"""\n\n    template_name = "my_payment_template.html"\n\n    def get_context_data(self, **kwargs):\n        """Add payment type to context data"""\n        kwargs = super().get_context_data(**kwargs)\n        kwargs["pro_plan"] = DRPaymentTypeModel.objects.filter(\n            description="Pro Plan"\n        ).first()\n        return kwargs\n```\n\n3. In your template, add your button wherever you wish for it to appear as follows:\n\n```python\n{% include \'djangorave/pay_button.html\' with payment_model=pro_plan %}\n```\n\n`Note:` You can add multiple buttons to a single template by simply adding multiple\nplans to your context data and then including each of them with their own `include`\ntag as above.\n\n4. Add the following script to your django base template (or anywhere in your template heirarchy that ensures it is loaded before your payment buttons):\n\n```html\n<script src="{% static \'djangorave/js/payment.js\' %}"></script>\n```\n\n# Button Styling\n\nThe following css classes are available for styling your payment buttons:\n\n- `rave-pay-btn` will apply to all buttons.\n- `rave-subscription-btn` will apply to recurring payment types (ie: those with a `payment_plan`).\n- `rave-onceoff-btn` will apply to once off payment types (ie: those without a `payment_plan`).\n\n# Transaction Detail Page\n\nFollowing a user payment, they will be redirected to the transaction detail page\nlocated at `/djangorave/<str:reference>/`\n\nA default transaction detail template is already available, however if you want\nto override it, you may do so by creating a new template in your root\ntemplates directory, ie: `/templates/djangorave/transaction.html`\n\nYou will have access to `{{ transaction }}` within that template.\n\n# Development\n\nIf you wish to contribute to the project, there is an example app that demonstrates\ngeneral usage.\n\n### Running the example:\n\n```bash\ngit clone https://github.com/bdelate/django-rave.git\ncd django-rave\nmake build\nmake migrate\nmake import\nmake dup\n```\n\nThere is a section at the bottom of `django-rave/example/example/settings.py`. Ensure the values are set accordingly:\n\n```python\nRAVE_PRODUCTION_PUBLIC_KEY = "your key"\nRAVE_PRODUCTION_SECRET_KEY = "your key"\nRAVE_SANDBOX_PUBLIC_KEY = "your key"\nRAVE_SANDBOX_SECRET_KEY = "your key"\nRAVE_SANDBOX = True\n```\n\nFlutterwave Rave requires payments to be associated with users who have an email address.\nTherefore, create and login with a new django user or use the existing user already\ngenerated following the above import command:\n\n```\nusername: testuser\npassword: secret\n```\n\nNavigate to http://localhost:8000/',
    'author': 'Brendon Delate',
    'author_email': 'brendon.delate@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bdelate/django-rave.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
