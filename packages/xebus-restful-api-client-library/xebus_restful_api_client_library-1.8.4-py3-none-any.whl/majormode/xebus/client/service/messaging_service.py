# Copyright (C) 2019 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from majormode.perseus.client.service.base_service import BaseService
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.obj import Object


class MessagingService(BaseService):
    BaseService._declare_custom_exceptions({
    })

    def send_message_to_child_guardians(
            self,
            child_account_id,
            l10n_message):
        """
        Send a direct message to the guardians of a child.


        :param child_account_id: Identification of the child to send the
            message to his guardians.

        :param l10n_message: A dictionary of localized messages where the key
            corresponds to an object `Locale` and the value to the textual
            message written in this locale.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/message/child/(child_account_id)/guardian',
                url_bits={
                    'child_account_id': child_account_id,
                },
                message_body=l10n_message,
                authentication_required=True,
                signature_required=True))

    def send_message_to_children_onboard_guardians(
            self,
            device_id,
            l10n_message):
        """
        Send a direct message to the guardians of children riding a school bus.

        These children have been checked-in by an attendant using an ID-Reader
        device.


        :param device_id: Identification of a the ID-R device of the attendant
            who checked-in the children who boarded the school bus.

        :param l10n_message: A dictionary of localized messages where the key
            corresponds to an object `Locale` and the value to the textual
            message written in this locale.
        """
        return Object.from_json(
            self.send_request(
                http_method=self.HttpMethod.POST,
                path='/message/child-onboard/(device_id)/guardian',
                url_bits={
                    'device_id': device_id,
                },
                message_body=l10n_message,
                authentication_required=True,
                signature_required=True))
