classDiagram
direction BT
class accounts_profilemanager {
   varchar(20) phone
   integer user_id
   integer id
}
class accounts_profilereferee {
   bigint referee_id
   integer user_id
   integer id
}
class auth_user {
   varchar(128) password
   datetime last_login
   bool is_superuser
   varchar(150) username
   varchar(150) last_name
   varchar(254) email
   bool is_staff
   bool is_active
   datetime date_joined
   varchar(150) first_name
   integer id
}
class competitions_city {
   varchar(64) name
   integer id
}
class competitions_competition {
   varchar(64) name
   varchar(64) category
   bigint level_id
   integer id
}
class competitions_competitioninseason {
   bigint competition_id
   bigint season_id
   integer id
}
class competitions_competitionlevel {
   varchar(64) name
   integer id
}
class competitions_match {
   varchar(10) code
   datetime date_time
   bigint city_id
   bigint competition_in_season_id
   bigint away_team_id
   bigint home_team_id
   integer id
}
class competitions_season {
   varchar(20) name
   date date_of_start
   date date_of_end
   integer id
}
class competitions_team {
   varchar(64) name
   varchar(64) contact_person
   varchar(20) phone
   varchar(254) e_mail
   bigint city_id
   bigint competition_in_season_id
   integer id
}
class delegations_delegation {
   varchar(5) referee_role
   bigint match_id
   bigint referee_id
   integer id
}
class referees_referee {
   varchar(32) name
   varchar(32) surname
   date date_of_birth
   real rating
   varchar(20) phone
   bigint city_id
   bigint licence_id
   integer id
}
class referees_refereelicence {
   varchar(5) name
   integer id
}
class referees_refereelicence_level {
   bigint refereelicence_id
   bigint competitionlevel_id
   integer id
}
class referees_unavailability {
   date date_from
   date date_to
   bigint referee_id
   integer id
}

accounts_profilemanager  -->  auth_user : user_id:id
accounts_profilereferee  -->  auth_user : user_id:id
accounts_profilereferee  -->  referees_referee : referee_id:id
competitions_competition  -->  competitions_competitionlevel : level_id:id
competitions_competitioninseason  -->  competitions_competition : competition_id:id
competitions_competitioninseason  -->  competitions_season : season_id:id
competitions_match  -->  competitions_city : city_id:id
competitions_match  -->  competitions_competitioninseason : competition_in_season_id:id
competitions_match  -->  competitions_team : home_team_id:id
competitions_match  -->  competitions_team : away_team_id:id
competitions_team  -->  competitions_city : city_id:id
competitions_team  -->  competitions_competitioninseason : competition_in_season_id:id
delegations_delegation  -->  competitions_match : match_id:id
delegations_delegation  -->  referees_referee : referee_id:id
referees_referee  -->  competitions_city : city_id:id
referees_referee  -->  referees_refereelicence : licence_id:id
referees_refereelicence_level  -->  competitions_competitionlevel : competitionlevel_id:id
referees_refereelicence_level  -->  referees_refereelicence : refereelicence_id:id
referees_unavailability  -->  referees_referee : referee_id:id
