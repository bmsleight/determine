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

<!-- No Inherit -->
div.Tramcar-Stop {width: 30px;
 height: 30px;
 background-color: black;
 background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeEAYAAABroHLhAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAAeAAAAHgD4T+E9AAADI0lEQVRYw91Zy64pURBd3c4EI4nHQOgEYwMzfIQJ8QH8gDDoiLkQP+IV4Q+8f0IkYmggEo8J6gz6lpZ7ruPR2OeeNVnpePRavaurateW6A9gEIfD4XA4AMPhcDgcAp1Op9Pp6NfT6XQ6nQLL5XK5XOq/s9lsNpsN8Pl8Pp8PiEaj0WgUiMVisVgMiEQikUgEMJlMJpPJqEoA9CC22+12uyUqFovFYpHI4XA4HA5+cM9jp9PpdDqJSqVSqVTS7/so7jZcrVar1SqR2+12u93PN3iNvV6v1+slqtVqtVrtBYa1UCVSVVVV1fcbvMSSJEmSRJTP5/P5vK7zYcP8B/F4PB6Pizd4jROJRCKRIDoej8fj8QHDP21Fb2Ve8ZsN1+v1er0uXvijzKHeaDQajcY3hjn7iUpGz2aPx+PxeIh2u91ut/uHYS4vooU+m7mcnQzv9/v9fq/XO9ECn80ul8vlculJGN1ut9vtihf2au73+/1+n+ij3W63222cwK2elub16/8F3LpqyVe/PvkMh8PhcJjIYrFYLBai+Xw+n8+JNpvNZrO5r4v5CWDd7IN9aT06EbgHTqfT6XSaaL1er9dr0bKNg32kUqlUKqXnKHm1Wq1WK8But9vtdsBqtVqtVtGBaRzsIxAIBAIBgH3K/IXFYrFYLACtHouWaxxaaAOTyWQymZx9wCH9297h2Ww2m82IzGaz2WzWQ/qDl3w8Ho/HYyAYDAaDQUDbNAB+v9/v94ter9vBK8pZWuu0gFAoFAqFAGSz2Ww2K75OvppzuVwulyNCr9fr9XriBb2aB4PBYDA4ay25BRMt7Nn8d2sp83Ask8lkMhn8OmihDMiyLMsy8GV7yNuqVz3xd7GiKIqifLM9ZPAAgDfSooXfy6y72Ww2m82vZQt0ATwqEW3gXi4UCoVC4XKdvmiYh2E8HBNt5Bonk8lkMmlgiMfg7MYr/lNCnXXwil4zerPhS+84D8TfbZTv22q1Wq3WveofMMzgrF4ul8vl8uvqOP9vpVKpVCrGj1qkk3OD0EIKGI1Go9FInzDcepjGPT0fnvFhmjagOKujBvEJVl1O2MNrVeYAAAAASUVORK5CYII=);
 color: white;
}

div.Tramcar-Proceed {width: 30px;
 height: 30px;
 background-color: black;
 background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeEAYAAABroHLhAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAAeAAAAHgD4T+E9AAADh0lEQVRYw92Zy44xURSFt2OCiRhgIEiEh8BDECEewGUkQiJxHYnEJUJ4C7cI74CHIBIRAyYicZuw/0H1Vp3urnZP5e9vclJO1am1qtSpXetI8AN4ktPpdDqdAAaDwWAwAOj3+/1+n9+eTqfT6RRgvV6v12v+OJVKpVKpAEwmk8lkArDb7Xa7HcDhcDgcDgCbzWaz2QCkUqlUKn1WJQDgg+z3+/1+j5jP5/P5PKJarVar1XTh+JYzhBgMBoPBIGI8Ho/H4/w29X89jlqNRqPRaBCLxWKxWOTP+yh3G240Go1GA1Gn0+l0OmGhCoVCoVAgzufz+XyOuNvtdrsdPw5tUz/tLzQetQaDwWAwIDabzWaz+QbD3F8VMZFIJBKJ64Ko9fv9fr8fcbvdbrdb4fGp3+fz+Xy+28eXSCQSiQQxlUqlUile58OGaQC32+12u28XQi1doFuhR+Pe81Dr8Xg8Hg/i+Xw+n8/C52FCz3Y6nU6n0wDtdrvdbr9gsngzrVar1WoBZDKZTCYjvN83w2SwUCgUCgWxbdwP908B6HQ6nU7nF8OHw+FwOABEIpFIJCK27Mf5eFIhGo1Go1GA4/F4PB5/MFyr1Wq1GsBisVgsFmLLfh5u9geo1+v1ev2TYSoYqtVqtVoVW+brqVQqlUoFgJvMABhVQqvVarVaiS3v9SyXy+VyCTAcDofDIQDr9Xq9Xk9sWe+HfLLRaDQajcSW837IJ5tMJpPJRGw572c8Ho/HYwC22Ww2m43Yct4P+WTPD/V/wZRKpVKpFFvG+yGfzGw2m81mseW8H4vFYrFYABglCn8dq9VqtVoBGEUpfx2n0+l0Oj/dYa1Wq9VqxZb1esjX5Q5TOEZfF3+NWCwWi8UAGGOMsU+vpXA4HA6HAfR6vV6vF1vm8xiNRqPRCBAKhUKhEP/7xbBcLpfL5fzXBZcZiS37fkg3+ZDJZDKZ7AfDBJdhASSTyWQyKbb8+6FoyuVyuVyu7/2ClVYul8vlcgBcOCa2jet4vV6v1wuQzWaz2ewvO94a01IcSvEoHS3UUuz6NY9+dUzLhXbX08qrMa0QXDrIB+JCgm4N4mez2Ww2Q+TmkNuD+G632+1271X/gGGCljxKpVKpVELk3nfCSy2BQCAQCCByaSgf1HM1rrBBGrdcLpfL5eeXWiQX509CmRFFKZQw3LqYRjU9FUJUAV4Kho/36LP8A0CqmRA8Il73AAAAAElFTkSuQmCC);
 color: white;
}

div.Tramcar-do-not-Proceed {width: 30px;
 height: 30px;
 background-color: black;
 background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeEAYAAABroHLhAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAAeAAAAHgD4T+E9AAADIklEQVRYw+VZy6riQBCtRNCluFAXooLkJ9Q/8L1Q8h0+FkHcCIIP/BFfBF2L4nMR/AZ/QRAxG7VmkSlzuTNejencXGbO5mDA7nPSnarqag5/A0zier1er1eAzWaz2WwAJpPJZDLRf+/3+/1+D3A4HA6Hg/4/j8fj8XgAIpFIJBIBiMfj8XgcIJvNZrNZgFgsFovFABwOh8PhMKsSAPBNnM/n8/mM2Gw2m80motfr9Xq99OLYsc/n8/l8iO12u91u6/O+C8OGe71er9dDDAQCgUCAvcFnHAqFQqEQYr/f7/f7FhjWtiqiJEmSJH2/wUfMcRzHcYjVarVareo63zZMA+Tz+Xw+b7/BZ1woFAqFAuLtdrvdbm8Y/mkr+irTir9seDAYDAYD+4W/y7TVh8PhcDj8wjBFP7uCEWsOBoPBYBBRVVVVVf9imNKL3UJZM6Wzu+HL5XK5XPR8Z7dA1uz3+/1+vx6EYbFYLBYL6ybM5XK5XA5xPp/P53PE0+l0Op10pueZTCaTyVinY7VarVYrRCiVSqVSif0ErVar1WoZKQk0NBqNRqPBXk+lUqlUKogQjUaj0Si7gbUa2LjRz0in0+l0mp0urUZHBNY1MG1Rs5jNZrPZjJ2ue4xyOp1Op5PdwPRtmsXxeDwej+x0uVwul8uFyMN/Bt7tdrvdbnYDKoqiKIr5cXa73W63Y6fr7pN10KJgYxbJZDKZTFoQtMrlcrlcZp8GKL0YRb1er9frFqal5XK5XC6tS/ipVCqVSulRl4IR8XQ6nU6niIlEIpFIWKdjvV6v1+sPpSWVYFZNaBd/Li15ao4Vi8VisQj/HLStDMDzPM/zAPfTEh0P6Vhl1Rv/Lg6Hw+Fw+IvjIYEaAHSQtlu4USbdo9FoNBr9GRQBH4BaJXYbMMq1Wq1Wqz3OAg8NUzOMmmN2G3nGoiiKomiiiUeg6EYr/lO2OumgFX1m9GXDj75xaoh/t1GaV5ZlWZaNqn/DMIGieqfT6XQ61uVxGrfb7Xa7XfNXLdzduUloWwpgu91ut1uA8Xg8Ho9fv0wTBEEQBP3yjC7TtFr/Qx41iV/ygAv4UelVPgAAAABJRU5ErkJggg==);
 color: white;
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
    <xsl:if test="$state = 'Tramcar-Stop'">
      <div class="state-abbr"></div>
    </xsl:if>
    <xsl:if test="$state = 'Tramcar-Proceed'">
      <div class="state-abbr"></div>
    </xsl:if>
    <xsl:if test="$state = 'Tramcar-do-not-Proceed'">
      <div class="state-abbr"></div>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
