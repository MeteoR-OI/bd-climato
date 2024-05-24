drop MATERIALIZED VIEW x_max_month;
drop MATERIALIZED VIEW x_max_day;
drop MATERIALIZED VIEW x_min_month;
drop MATERIALIZED VIEW x_min_day;
drop MATERIALIZED VIEW obs_month;
drop MATERIALIZED VIEW obs_day;
drop MATERIALIZED VIEW obs_hour;
drop table x_min;
drop table x_max;
drop table obs;
drop table postes;
drop table mesures;
drop table incidents;
drop table annotations;

drop table django_admin_log;
drop table django_migrations;
drop table django_content_type cascade;

drop table auth_user_user_permissions;
drop table auth_user_groups;
drop table auth_group_permissions;
drop table auth_group;
drop table auth_permission;
drop table auth_user;
drop table django_session;

vacuum full;
