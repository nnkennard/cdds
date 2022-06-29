import collections


def review_getter_main(forum_notes):
  return [x for x in forum_notes if "review" in x.content]


def review_getter_alternate(forum_notes):
  return []  # ???


Venue = collections.namedtuple("Venue",
                               "conference_name invitation_url review_getter")

venues = [
    Venue(
        "midl_2020",
        "MIDL.io/2020/Conference/-/Blind_Submission",
        review_getter_alternate,
    ),
    Venue(
        "corl_2021",
        "robot-learning.org/CoRL/2021/Conference/-/Blind_Submission",
        review_getter_main,
    ),
    Venue(
        "uai_2022",
        "auai.org/UAI/2022/Conference/-/Blind_Submission",
        review_getter_main,
    ),
    Venue("iclr_2018", "ICLR.cc/2018/Conference/-/Blind_Submission",
          review_getter_main),
    Venue("iclr_2019", "ICLR.cc/2019/Conference/-/Blind_Submission",
          review_getter_main),
    Venue("iclr_2020", "ICLR.cc/2020/Conference/-/Blind_Submission",
          review_getter_main),
    Venue("iclr_2021", "ICLR.cc/2021/Conference/-/Blind_Submission",
          review_getter_main),
    Venue("iclr_2022", "ICLR.cc/2022/Conference/-/Blind_Submission",
          review_getter_main),
    Venue(
        "neurips_2021",
        "NeurIPS.cc/2021/Conference/-/Blind_Submission",
        review_getter_main,
    ),
]
