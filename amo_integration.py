from datetime import datetime

from amocrm.v2 import (
    Lead,
    Contact as _Contact,
    custom_field,
    Tag,
    Task
)


class Contact(_Contact):
    post = custom_field.TextCustomField("Должность")
    phone = custom_field.ContactPhoneField("Телефон")
    email = custom_field.ContactEmailField("Email")


class Person:
    def __init__(self, first_name, contact_phone):
        self.first_name = first_name
        self.contact_phone = contact_phone


def add_deal(
        lead_name,
        user_id,
        status,
        person,
        task_date,
        task_text,
        tags=None
):
    new_lead = Lead.objects.create(
        name=lead_name,
        responsible_user_id=user_id,
        status_id=status
    )

    if tags:
        lead_tag_manager = Tag.leads
        for tag_name in tags:
            tag = lead_tag_manager.create(name=tag_name)
            new_lead.tags.append(tag)

    new_lead.save()

    if person.first_name:
        new_contact = Contact.objects.create(responsible_user_id=10698318)
        new_contact.first_name = person.first_name
        if person.contact_phone is not None:
            new_contact.phone = person.contact_phone

        new_contact.save()

        new_lead.contacts.append(new_contact)

    new_lead.save()

    complete_till_timestamp = None
    if isinstance(task_date, str):
        task_datetime = datetime.strptime(task_date, "%Y-%m-%dT%H:%M:%S%z")
    else:
        task_datetime = task_date

    complete_till_timestamp = int(task_datetime.timestamp())

    if complete_till_timestamp is not None:
        new_task = Task.objects.create(
            entity_id=new_lead.id,
            entity_type="leads",
            complete_till=complete_till_timestamp,
            text=task_text if task_text else '',
            responsible_user_id=user_id
        )

        new_task.save()
