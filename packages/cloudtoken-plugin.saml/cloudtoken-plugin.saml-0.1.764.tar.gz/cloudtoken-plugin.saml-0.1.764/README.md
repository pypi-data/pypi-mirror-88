# cloudtoken-saml-plugin

Cloudtoken auth plugin that processes a SAML assertion provided by the previous plugin and displays a list of Federated Roles to choose from.

The SAML plugin will look for SAMLResponse data passed from a previous plugin (looking for the key "contains_samlresponse" = True in the data payload).
If the SAML pllugin can't find a plugin stating it has a SAMLResponse it will attempt to load the SAMLResponse from the previous plugins data payload.

## Installation

    $ pip3 install cloudtoken-saml-plugin

    # Add plugin to cloudtoken config, example:
    $ vi ~/.config/cloudtoken/config.yaml
    defaults:
      saml:
        saml_response_plugin: centrify  # <-- example, replace with the plugin that supplies your SAMLResponse.
    plugins:
        pre_auth:
        auth:
            - idp
            - saml  # <-- here.
        post_auth:
            - export_credentials_json
            - export_credentials_shell
            - export_credentials_awscli   

## Contributors

Pull requests, issues and comments welcome. For pull requests:

* Add tests for new features and bug fixes
* Follow the existing style
* Separate unrelated changes into multiple pull requests

See the existing issues for things to start contributing.

For bigger changes, make sure you start a discussion first by creating
an issue and explaining the intended change.

Atlassian requires contributors to sign a Contributor License Agreement,
known as a CLA. This serves as a record stating that the contributor is
entitled to contribute the code/documentation/translation to the project
and is willing to have it used in distributions and derivative works
(or is willing to transfer ownership).

Prior to accepting your contributions we ask that you please follow the appropriate
link below to digitally sign the CLA. The Corporate CLA is for those who are
contributing as a member of an organization and the individual CLA is for
those contributing as an individual.

* [CLA for corporate contributors](https://na2.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=e1c17c66-ca4d-4aab-a953-2c231af4a20b)
* [CLA for individuals](https://na2.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=3f94fbdc-2fbe-46ac-b14c-5d152700ae5d)

## License

Copyright (c) 2016 Atlassian and others.
Apache 2.0 licensed, see [LICENSE.txt](LICENSE.txt) file.
