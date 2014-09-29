django-draft-model
==================

Manages creation, editing and publishing of drafts model objects for editing.

Aims
====

* Mark model with decorator
* Model will be given a foreign key to the model automatically
* Upon updating the model the draft will be changed instead
* Upon calling publish on the model the draft information will be saved in the main instance
* creation_date field will be added to the model which will be populated when the model is first made
* edited_date field will be added to the model which will be updated when the field is updated
* Drafts will have simple migrations applied to them automatically

