# [TERR] WKB Contour Lines
# Draw contour lines on a surface using local polynomial regression smoothing

# Inputs:
#	x - column of real values indicating x coordinates or longitudes
#	y - column of real values indicating y coordinates or latitudes
#	z - column of real or integer valued data 
#	smooth.scale - (value) Optional real number between 0 and 1 value controlling the degree of smoothness

# Output:
#	contours - table with 2 columns:
#		Level - the contour line level
#		Geometry - WKB binary representation of the contour line

# Peter Shaw, Ian Cook
# "Fri Sep 09 12:30:05 2016"


# ----- Save Data Snapshot ------------------------------------------------------------------------------
# Save a snapshot of the environment to an RData file for code development.  Comment out when finished:
#TimeStamp=paste(date(),Sys.timezone())
#if(file_test("-d", "C:/Temp")) suppressWarnings(try(save(list=ls(), file="C:/Temp/contour.in.RData", RFormat=T )))
# remove(list=ls()); load(file='C:/Temp/contour.in.RData'); print(TimeStamp) # use in development


# --- Function definitions ----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
InOut.contour.points=function(x.cont0, y.cont0, xref.vec, yref.vec){
  # Peter Shaw
  N.cont = length(x.cont0)
  N.ref  = length(xref.vec)
  x.cont = c(x.cont0,x.cont0[1])
  y.cont = c(y.cont0,y.cont0[1])
  u=1:N.cont
  vec1.x = rep(1,N.ref) %o% x.cont[u]   - xref.vec %o% rep(1,N.cont)
  vec2.x = rep(1,N.ref) %o% x.cont[u+1] - xref.vec %o% rep(1,N.cont)
  vec1.y = rep(1,N.ref) %o% y.cont[u]   - yref.vec %o% rep(1,N.cont)
  vec2.y = rep(1,N.ref) %o% y.cont[u+1] - yref.vec %o% rep(1,N.cont)
  Vec1xVec2 = vec1.x*vec2.y-vec2.x*vec1.y
  Vec1dVec2 = vec1.x*vec2.x+vec1.y*vec2.y
  Ang = atan2( Vec1xVec2, Vec1dVec2 )
  angle.sums = rowSums(Ang)/(2*pi)
  return( round(abs(angle.sums)*1000)/1000 )
}
# -----------------------------------------------------------------------------------------------------------
ContourListToWKBLineStrings <- function(contourList) {
#	Ian Cook
  wkb <- lapply(contourList, function(coords) {
    if(length(coords$x) < 1) {
      thisOutput <- as.raw(c(1,2,0,0,0,0,0,0,0))
    } else {
      rc <- rawConnection(raw(0), "r+")
      writeBin(as.raw(c(1,2,0,0,0)), rc)
      writeBin(length(coords$x), rc, size=4)
      mapply(coords$x, coords$y, FUN=function(x,y) {
        writeBin(as.double(x), rc, size=8)
        writeBin(as.double(y), rc, size=8)
        NULL
      })
      thisOutput <- rawConnectionValue(rc)
      close(rc)
    }
    thisOutput
  })
  attr(wkb, "SpotfireColumnMetaData") <-
    list(ContentType = "application/x-wkb", MapChart.ColumnTypeId = "Geometry")
  I(wkb)
}
# --- End function definitions ------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------

if(is.null(smooth.scale)) smooth.scale=0.5

# prepare null output
contours <- data.frame(
  Level=as.numeric(NA),
  Geometry=ContourListToWKBLineStrings(list(list(level=NA,x=NA,y=NA)))
)

xyzdata = data.frame( x=x, y=y, z=z )
bad = is.na(x) | is.na(x) | is.na(z)
xyzdata = xyzdata[!bad,]

xyzdata.lo <- try(loess(z~x*y, data=xyzdata, span=smooth.scale, na.action=na.exclude))
ok = attr(xyzdata.lo,"class")!= "try-error"

if(ok){
  xvec = seq(from=min(x,na.rm=T), to=max(x,na.rm=T), length=200)
  yvec = seq(from=min(y,na.rm=T), to=max(y,na.rm=T), length=200)
  xyzdata.lo.pred <- predict( xyzdata.lo, newdata=expand.grid(x=xvec, y=yvec))
  
  x.mtx = xvec %o% rep(1,length(yvec))
  y.mtx = rep(1,length(xvec)) %o% yvec
  
  points.chull <- chull(xyzdata$x, xyzdata$y)
  
  mtx.inout.vec = InOut.contour.points(
    x.cont0 = xyzdata$x[points.chull],
    y.cont0 = xyzdata$y[points.chull],
    xref.vec=as.numeric(x.mtx), 
    yref.vec=as.numeric(y.mtx)
  )
  xyzdata.lo.pred[mtx.inout.vec==0]=NA
  
  xyzdata.lo.pred = pmin(xyzdata.lo.pred,max(z,na.rm=T))
  xyzdata.lo.pred = pmax(xyzdata.lo.pred,min(z,na.rm=T))
  
  points.chull.closed = c(points.chull,points.chull[1])
  x.chull = xyzdata$x[points.chull.closed]
  y.chull = xyzdata$y[points.chull.closed]
  
  contourLevels <- pretty(xyzdata.lo.pred,20)
  
  contourList <- contourLines(x=xvec, y=yvec, z=xyzdata.lo.pred, levels=contourLevels)
  
  contourList[[length(contourList)+1]] <- 
    list(
      level=NA,
      x=x.chull,
      y=y.chull
    )
  
  contourLines <- ContourListToWKBLineStrings(contourList)
  
  contours <- data.frame(
    Level=sapply(contourList,function(x){x$level}),
    Geometry=contourLines
  )
}
# [TERR] WKB Contour Lines