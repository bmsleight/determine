<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html" version="1.0" encoding="iso-8859-1" indent="yes"/>
  <xsl:template match="/">
    <head>
    <title><xsl:value-of select="/traffic_signals_report/address"/></title>
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

</style>
    </head>


<h1><xsl:value-of select="/traffic_signals_report/address"/></h1>
<xsl:apply-templates select="/traffic_signals_report/diagrams/diagram"/>
<xsl:call-template name="key"/>
</xsl:template>


<xsl:template match="diagram">
<xsl:variable name="diagram" select="."/>
    <div class="site-header">
      <span size="larger">
        <p>
          <u>Diagram: <xsl:value-of select="$diagram/title"/></u>
        </p>
      </span>
    </div>
    <table class="signals">
      <tr>
        <td> </td>
        <xsl:for-each select="$diagram/times/time/t">
          <xsl:sort data-type="number" select="."/>
          <xsl:variable name="t" select="."/>
          <xsl:if test="string-length($t) &gt; 2">
            <th>
              <xsl:value-of select="."/>
            </th>
          </xsl:if>
          <xsl:if test="string-length($t) = 2">
            <th> <xsl:value-of select="."/></th>
          </xsl:if>
          <xsl:if test="string-length($t) &lt; 2">
            <th> <xsl:value-of select="."/> </th>
          </xsl:if>
        </xsl:for-each>
      </tr>
      <xsl:for-each select="$diagram/times/time[t=0]/phases/phase">
        <xsl:sort/>
        <tr>
          <xsl:variable name="letter" select="letter"/>
          <td>
            <xsl:value-of select="$letter"/>
          </td>
          <xsl:for-each select="$diagram/times/time/t">
            <xsl:sort data-type="number" select="."/>
            <xsl:variable name="t" select="."/>
            <xsl:variable name="st" select="$diagram/times/time[t=$t]/phases/phase[letter=$letter]/state"/>
            <td>
              <div>
                <xsl:attribute name="class">
                  <xsl:value-of select="$st"/>
                </xsl:attribute>
                <xsl:apply-templates select="$diagram/times/time[t=$t]/phases/phase[letter=$letter]/state"/>
              </div>
            </td>
          </xsl:for-each>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>

  <xsl:template name="key">
    <p><u>Key</u></p>
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
  </xsl:template>
</xsl:stylesheet>
