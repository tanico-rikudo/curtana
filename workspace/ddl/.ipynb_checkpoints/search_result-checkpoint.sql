CREATE  Table elica.SEARCH_RESULT
(REPORT_ID int auto_increment,
 SUBMIT_DT varchar(32) not null,
 SUBMIT_TYPE varchar(64) not null,
 EDINET_CODE varchar(32) not null,
 SUBMITTER_NAME varchar(64) not null,
 DETAIL_URL varchar(512),
 PDF_URL varchar(512),
 XBRL_URL varchar(512),
 FETCH_DT DATETIME not null,
 SUCCESS_FLG BOOLEAN not null,
 CRETAE_DT DATETIME not null,
 UPDATE_DT DATETIME not null,
 PRIMARY KEY(REPORT_ID)
 );
 commit;
