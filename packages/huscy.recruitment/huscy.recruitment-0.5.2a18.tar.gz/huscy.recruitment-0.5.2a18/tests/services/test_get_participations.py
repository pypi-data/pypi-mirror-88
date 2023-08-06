import pytest

from model_bakery import baker

from huscy.recruitment.services import get_participations

pytestmark = pytest.mark.django_db


def test_get_participations_without_arguments():
    with pytest.raises(ValueError):
        get_participations()


def test_get_participations_by_project(attribute_filterset, participation):

    # check one exists by default
    participations = get_participations(attribute_filterset=attribute_filterset)
    assert len(participations) == 1

    # make 3 more for the same project and check there are 4
    baker.make('recruitment.Participation', attribute_filterset=attribute_filterset, _quantity=3)
    participations = get_participations(attribute_filterset=attribute_filterset)
    assert len(participations) == 4

    # make 3 for different project and check there are still 4
    second_attribute_filterset = baker.make('recruitment.AttributeFilterSet')
    baker.make('recruitment.Participation', attribute_filterset=second_attribute_filterset,
               _quantity=3)
    participations = get_participations(attribute_filterset=attribute_filterset)
    assert len(participations) == 4


def test_get_participations_by_subject(subject, attribute_filterset, participation_content_type,
                                       participation):

    # check one exist by default
    participations = get_participations(subject=subject)
    assert len(participations) == 1

    # make one for different attribute filterset and check there is still 1
    baker.make('recruitment.Participation', attribute_filterset=attribute_filterset, _quantity=3)
    participations = get_participations(subject=subject)
    assert len(participations) == 1

    # make one more participation for the different attribute_filterset and check there are 2
    second_attribute_filterset = baker.make('recruitment.AttributeFilterset')
    pseudonym = baker.make('pseudonyms.Pseudonym', subject=subject,
                           content_type=participation_content_type)
    baker.make('recruitment.Participation', attribute_filterset=second_attribute_filterset,
               pseudonym=pseudonym.code)

    participations = get_participations(subject=subject)
    assert len(participations) == 2


def test_get_participations_by_subject_and_attribute_filterset(subject, participation_content_type,
                                                               participation):
    # check one exists by default
    participations = get_participations(subject=subject,
                                        attribute_filterset=participation.attribute_filterset)
    assert len(participations) == 1

    # make one for different attribute filterset and check there is 1
    second_attribute_filterset = baker.make('recruitment.AttributeFilterSet')
    baker.make('recruitment.Participation', attribute_filterset=second_attribute_filterset)

    participations = get_participations(subject=subject,
                                        attribute_filterset=participation.attribute_filterset)
    assert len(participations) == 1

    # make one participation for subject within diffrent attribute_filterset and check there is 1
    pseudonym = baker.make('pseudonyms.Pseudonym', subject=subject,
                           content_type=participation_content_type)
    baker.make('recruitment.Participation', attribute_filterset=second_attribute_filterset,
               pseudonym=pseudonym.code)

    participations = get_participations(subject=subject,
                                        attribute_filterset=participation.attribute_filterset)
    assert len(participations) == 1

    # make one participation for subject for the same attribute_filterset and check there are 2
    ps2 = baker.make('pseudonyms.Pseudonym', subject=subject,
                     content_type=participation_content_type)
    baker.make('recruitment.Participation', attribute_filterset=participation.attribute_filterset,
               pseudonym=ps2.code)
    participations = get_participations(subject=subject,
                                        attribute_filterset=participation.attribute_filterset)
    assert len(participations) == 2
