<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html" version="1.0" encoding="iso-8859-1" indent="yes"/>
  <xsl:template match="/">
    <head>
      <title>
        <xsl:value-of select="/traffic_signals_report/address"/>
      </title>
      <style type="text/css">
p {margin-left: 20px}

<!--Set master Red, Green, Amber, Red-Amber -->
div.Red {
 width: 30px;
 height: 30px;
 background-color: red;
 color: red;
}

div.Amber {
 width: 30px;
 height: 30px;
 background-color: DarkOrange;
 color: DarkOrange;
}

div.Green { width: 30px;
 height: 30px;
 background-color: green;
 color: green;
}

div.Red-Amber { 
 width: 30px;
 height: 30px;
 background-color: red;
 background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAeEAYAAAC9BaiEAAAABmJLR0T//wAAAADX49c/AAAACXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAABAAAAHgAKz1FzAAAAHUlEQVQY02P4/5+BgYHh/38mBigYKEZPz0DaDgEA0Y4FT7mx5WcAAAAASUVORK5CYII=);
 color: Tomato;
 font-weight: bold;
}


div.Off {
 width: 30px;
 height: 30px;
 background-color: black;
 color: white;
}

div.On {
 width: 30px;
 height: 30px;
 background-color: white;
 color: black;
}



<!-- Inherit Green -->
div.Arrow { 
 color: black;
}

<!-- No Inherit -->
div.Arrow.Off {
 width: 30px;
 height: 30px;
 background-color: black;
 color: white;
}

<!-- No Inherit -->
div.Black-Out {width: 30px;
 height: 30px;
 background-color: black;
 color: black;
}

<!-- Inherit Green and Red-->
div.Man { 
 color: black;
}


div.state-abbr {
line-height:30px;
text-align: center;
}

div.stage {
 line-height:30px;
 text-align: center;
}


div.running {
 background-color: white;
 color: black;
}

div.min {
 color: red;
}

div.movingto {
 background-color: grey;
 color: black;
}


table.signals {
	border-width: 0px 0px 0px 0px;
	border-spacing: 2px;
	border-style: solid solid solid solid;
	border-color: black black black black;
	border-collapse: collapse;
	background-color: white;
        margin-left: 20px;
}
table.signals th {
	border-width: 1px 1px 1px 1px;
	padding: 2px 2px 2px 2px;
	border-style: inset inset inset inset;
	border-color: gray gray gray gray;
	background-color: white;
	-moz-border-radius: 0px 0px 0px 0px;
        font-size: x-small;
}
table.signals td {
	border-width: 1px 1px 1px 1px;
	padding: 0px 0px 0px 0px;
	border-style: inset inset inset inset;
	border-color: gray gray gray gray;
	background-color: white;
	-moz-border-radius: 0px 0px 0px 0px;
}

div.time {
position:relative;
left:-17px
}

div.key-title {
 text-decoration: underline;
 padding: 20px 0px 5px 20px;
}

div.site-header {
 text-decoration: underline;
 font-size: large;
 padding: 30px 0px 15px 20px;
}

div.comments {
 font-size: small;
 padding: 30px 0px 15px 20px;
}


</style>
    </head>
    <h1>
      <xsl:value-of select="/traffic_signals_report/address"/>
    </h1>
    <xsl:apply-templates select="/traffic_signals_report/diagrams/diagram"/>
    <xsl:call-template name="key"/>
  </xsl:template>
  <xsl:template match="diagram">
    <xsl:variable name="diagram" select="."/>
    <div class="site-header">
      <u>Diagram: <xsl:value-of select="$diagram/title"/></u>
    </div>
    <table class="signals">
      <tr>
        <td> </td>
        <xsl:for-each select="$diagram/times/time/t">
          <xsl:sort data-type="number" select="."/>
          <xsl:variable name="t" select="."/>
          <xsl:if test="$t &gt; -1">
            <xsl:if test="string-length($t) &gt; 2">
              <th>
                <div class="time">
                  <xsl:value-of select="."/>
                </div>
              </th>
            </xsl:if>
            <xsl:if test="string-length($t) = 2">
              <th>
                <div class="time">  <xsl:value-of select="."/></div>
              </th>
            </xsl:if>
            <xsl:if test="string-length($t) &lt; 2">
              <th>
                <div class="time"> <xsl:value-of select="."/> </div>
              </th>
            </xsl:if>
          </xsl:if>
        </xsl:for-each>
      </tr>
      <xsl:for-each select="$diagram/times/time[t=0]/phases/phase">
        <xsl:sort/>
        <tr>
          <xsl:variable name="letter" select="letter"/>
          <td>
             &#160;<xsl:value-of select="$letter"/>
          </td>
          <xsl:for-each select="$diagram/times/time/t">
            <xsl:sort data-type="number" select="."/>
            <xsl:variable name="t" select="."/>
            <xsl:variable name="st" select="$diagram/times/time[t=$t]/phases/phase[letter=$letter]/state"/>
            <xsl:if test="$t &gt; -1">
              <td>
                <div>
                  <xsl:attribute name="class">
                    <xsl:value-of select="$st"/>
                  </xsl:attribute>
                  <xsl:apply-templates select="$diagram/times/time[t=$t]/phases/phase[letter=$letter]/state"/>
                </div>
              </td>
            </xsl:if>
          </xsl:for-each>
        </tr>
      </xsl:for-each>
      <tr>&#160;</tr>
      <tr>
        <td>Stage&#160;</td>
        <xsl:for-each select="$diagram/times/time/t">
          <xsl:sort data-type="number" select="."/>
          <xsl:variable name="t" select="."/>
          <xsl:variable name="st" select="$diagram/times/time[t=$t]/stage"/>
          <xsl:if test="$t &gt; -1">
            <td>
              <xsl:variable name="running" select="$diagram/times/time[t=$t]/stage/running"/>
              <xsl:if test="string-length($running) &gt; 0">
                <xsl:variable name="mins" select="sum($diagram/times/time[t=$t]/phases/*/min_remaining)"/>
                <xsl:if test="$mins &gt; 0">
                  <div class="stage running min">
                    <xsl:apply-templates select="$diagram/times/time[t=$t]/stage/running"/>
                  </div>
                </xsl:if>
                <xsl:if test="$mins &lt; 1">
                  <div class="stage running">
                    <xsl:apply-templates select="$diagram/times/time[t=$t]/stage/running"/>
                  </div>
                </xsl:if>
              </xsl:if>
              <xsl:if test="string-length($running) &lt; 1">
                <div class="stage movingto">
                  <xsl:apply-templates select="$diagram/times/time[t=$t]/stage/moving_to"/>
                </div>
              </xsl:if>
            </td>
          </xsl:if>
        </xsl:for-each>
      </tr>
    </table>
    <div class="comments">
      Comments:
      <xsl:variable name="stable" select="$diagram/stable"/>
      <xsl:if test="$stable = 'True'">
        This is a stable cycle.
      </xsl:if>
      <xsl:if test="$stable = 'False'">
        This is not a stable cycle, minimum times appear not be be satisfied. 
      </xsl:if>
    </div>
  </xsl:template>
  <xsl:template name="key">
    <div class="key-title">Key - Phases</div>
    <table class="signals">
      <tr>
        <th>Symbol</th>
        <th>Signal</th>
      </tr>
      <xsl:variable name="unique-list" select="//state[not(.=following::state)]"/>
      <xsl:for-each select="$unique-list">
        <xsl:sort select="."/>
        <tr>
          <td>
            <div>
              <xsl:attribute name="class">
                <xsl:value-of select="."/>
              </xsl:attribute>
              <xsl:apply-templates select="."/>
            </div>
          </td>
          <td>
             <xsl:value-of select="."/>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <div class="key-title">Key - Stages</div>
    <table class="signals">
      <tr>
        <th>Symbol</th>
        <th>Stage</th>
      </tr>
      <tr>
        <td>
          <div class="stage movingto">X</div>
        </td>
        <td>&#160;Moving to Stage X&#160;</td>
      </tr>
      <tr>
        <td>
          <div class="stage running min">X</div>
        </td>
        <td>&#160;Running minimums in Stage X&#160;</td>
      </tr>
      <tr>
        <td>
          <div class="stage running">X</div>
        </td>
        <td>&#160;Running Stage X&#160;</td>
      </tr>
    </table>
  </xsl:template>
  <xsl:template match="state">
    <xsl:variable name="state" select="."/>
    <xsl:if test="$state = 'Red'">
      <div class="state-abbr">R</div>
    </xsl:if>
    <xsl:if test="$state = 'Amber'">
      <div class="state-abbr">A</div>
    </xsl:if>
    <xsl:if test="$state = 'Green'">
      <div class="state-abbr">G</div>
    </xsl:if>
    <xsl:if test="$state = 'Red-Amber'">
      <div class="state-abbr">RA</div>
    </xsl:if>
    <xsl:if test="$state = 'Red Man'">
      <div class="state-abbr">r</div>
    </xsl:if>
    <xsl:if test="$state = 'Green Man'">
      <div class="state-abbr">g</div>
    </xsl:if>
    <xsl:if test="$state = 'Green Filter Arrow'">
      <div class="state-abbr">f</div>
    </xsl:if>
    <xsl:if test="$state = 'Right Turn Indicative Green Arrow'">
      <div class="state-abbr">I</div>
    </xsl:if>
    <xsl:if test="$state = 'Arrow Off'">
      <div class="state-abbr">.</div>
    </xsl:if>
    <xsl:if test="$state = 'Black-Out'">
      <div class="state-abbr">b</div>
    </xsl:if>
    <xsl:if test="$state = 'Off'">
      <div class="state-abbr">0</div>
    </xsl:if>
    <xsl:if test="$state = 'On'">
      <div class="state-abbr">1</div>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
