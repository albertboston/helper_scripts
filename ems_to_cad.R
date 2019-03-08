library(RODBC)

source("code/credentials.R")

vsql25 <- odbcConnect("vsql25", uid = vsql.uid, pwd = vsql.pwd)

ems.crash <- sqlQuery(vsql25, paste(
  "SELECT *",
  "FROM [EDW_Generic].[dbo].[EMS_Crash]"
))

ems.crash$IncidentNumber <- paste0("E", ems.crash$IncidentNumber)


cad <- odbcConnect("cad", uid = cad.uid, pwd = cad.pwd)

cad.crash <- sqlQuery(cad, paste(
  "SELECT ", 
  "[rec_x_cord] ",
  ",[rec_y_cord] ",
  ",[typ_eng] ",
  ",[tycod] ",
  ",[num_1] ",
  "FROM [CAD92Arch].[dbo].[agency_event] ",
  "WHERE ",
  "num_1 in ('",
  paste(ems.crash$IncidentNumber, collapse = "', '"),
  "');"
), sep = "")
