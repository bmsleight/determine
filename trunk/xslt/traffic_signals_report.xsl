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
 background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeEAYAAABroHLhAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAAeAAAAHgD4T+E9AAAAVUlEQVRYw+3SsQ0AMAgDQSfKYtTsP09SZAeQzH9B7ZNY90rSvxPa3QMAAwYMGDBgwHMC7B5g944U0T2iGJzZPaKycS8N2D3A7gF2D7B7gN0D7N448AMLLAVUo9WUXgAAAABJRU5ErkJggg==);
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
 width: 30px;
 height: 30px;
 background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeEAYAAABroHLhAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAAeAAAAHgD4T+E9AAACh0lEQVRYw92Zy06zUBSFd6sTYESCOjBqIryE+hBOIAbewujAGOdG44soGqNv4P0hJCaEIQPCAJyo5x/srlaav+HS1kO7B/04aQtrcTbnsukIQUTEn+PE9zfz5YV5f19sf3wwk6T4P11nbm4yd3aYu7vM7W3mwsK4CnsBw3WZ58zTU+bS0u8bNzkuLzPPzorXbaq7tuHLS+bq6nQMlnF9nXl1NSXDnKpCHB3JMTiKnQ7z+Lios7FhnMC222GwjI7D/PlpaLhtPVqV6PHKhn2/HcKbEql+fV1iGKOfrMFo0lxbY35+jjCM6UW20EkT01nf8NcXH2C+ky1w0lxZYWIQpoeHdgibNp+emIt3d1QIXdd1XSdyHMdxnEF7ViJJkiRJiHzf931/0O773Npi56qqqqoqRBRFURQJkWVZlmVi5gK64QO+eI0uRDcI2LjneZ7nDXqUfyi7v+oHdMOH67qu6xK9v/P33TTlA8MwDMMg0jRN0zTZsscP+LAsy7IsIvjs4gdxHMdxTJTnec5z8mwHpzZREAQBspiIiLCtm7dnOAzDMAyFUBRFUZTBtNvBoPX2xjcAuW/btm3bRKZpmqYpu7+qB3oUo3SapmmaDgoLdHDAhrk1vzw87LUfH9shaNp8fu61sbTEEky2sElzeGnZRXFsf5/mMjiVibqYj4a3h9hWVb2DbeXGBnPk9nC4AICNtGzhdQndNzdFXyMNgyiVyDZQlycn//dTahjFMBTHZBsp495eUXdtwyBGN/R4W1IdOtCjZUYrGx71jKMg/tdGcd3b23q6GxseHtXPz5nTmsdx3ouL4nWb6u70nY8ZnFJEr69MVBiqvkyzLCZenuFlGq/1f82jY8Y/AgzrM9JniNcAAAAASUVORK5CYII=);
 color: Black;
}

div.Tramcar-Proceed {width: 30px;
 height: 30px;
 background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeEAYAAABroHLhAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAAeAAAAHgD4T+E9AAAC5klEQVRYw+WZTU/qQBiFXxqNSk20laW6oUnrx9aPGDXRhca1ZVH8M/6f+gM0UTcaje41NmGl7MA2GFs0Gr2Lt+eWEuilcKWX3rN5Am3hPTPDzHAmQ3R4SPT9TT3r64v59MS0LObjI9NxmG9v4edGR5mSxJydZaoqc2aGKQi910g01P2jHx/Mmxvm9TXTdRvvkiRJkiSiQuHgoFAIXjuO4zgOkWmapmkSOU65zE1SLvOTV1dMUWSurTGXl5nDw91UnYnfw3d3zJMT5stLq7uy2Ww2myWyLMuyLCJZlmVZDt73PM/zPCLbtm3bJlJVVVXV4P32mphg7uwwFxbiGO5gmKAxTk+ZphllFCoWi8ViMehRGG1uEFw3DMMwjE5KrtWYR0fMs7NwnV0bxgfA4OVlnJbM5XK5XI5IFEURg7KVcF1RFEVR4nwD6ru4CDdAtPEIw2i5+/s4ZSQn/NTOz2MahsF4PfrvCHW37qgGw5h1j4+TLrk3YUhjUv38bGMYy0v0ZDQ4wuQGX78NY8OAdTRtgi/ueSHYGYU3DOnR6yuTfQpEDw9Jl9QfsU8h2MqlXexTILLtpEvpj56ffcPN/17Sqvd33/D/JSH4P5p2jYz4hmU56VL6o6kp3zAShbRreto3jCgl7dI03zB6eHw86ZJ+RvDFPoUgHFtdTbq0nxGysEzGNwytrDCRGQ26JieZCP1YDYaRAu7uNrbI4Al1w8dQKJltsfGYn2euryddenfa2GDOzbW6GrHT2t5mxotBk9PiInNrK+quCMMYGrrORMt1NtQrlUqlUvlzzuy6ruu6RKVSqVQqxTGIOjY3mfv7ndTXRRCPcAyZEaKUsDoN4qvVarVaJdI0TdM0onq9Xq/Xo74fk+reHpPX146bqfuzJYR+t7dMRClIGFgI2nVd13WdKJ/P5/P5oEdx1FKr1Wqtmw7rKJaXpSVm345a2gmfgcgISQpe4zCtuf/GxpjY02Mj1HyY9ndWjV+jYRVnKapExwAAAABJRU5ErkJggg==);
 color: Black;
}

div.Tramcar-do-not-Proceed {width: 30px;
 width: 30px;
 height: 30px;
 background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeEAYAAABroHLhAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAACXZwQWcAAAAeAAAAHgD4T+E9AAADsUlEQVRYw92ZTU9TQRSGnxYQMBJoCLiSEuMSla2VAEETtd8hGkzUuFc0fC4QNtWijSKJxn+AiQaQBBbKorYBxUXTjSZu0WhciBGkNGIiMC4m01YFodwpFZ7NpB/33vedO3PmzBmTEH19IAQGWV5eWQGYmnr/HmBs7O3b1M/T01+/AszNLS6mXmexFBYC7N9fWgpw9GhlJYDHU1UFYLNZrQA5OWazUY0Aps0aXlz8+RPg3r0XLwD6+ycnAb58icd1CFOUl+/ZA9DeXlcHcOVKTQ1AYWFe3pYYHhx8/RqgrW1sDODTp/l5nQbXo6KipASgr8/lAjhz5vDhdK5fd5isrMjO6Op6+hSgqWlgIBtGFR8+fPsmdTx8CNDd/exZqs5NG1Y3UAYDgVAoGwbXQgip7+bN588Bzp6VHaC+T9uw6rnh4Tdvsm1uIwwNyanW0zM+npZhZfB/e6Mb5dYtqfvJk9VfVMKwirotLaOj2RZtBDWkW1tlUP3xY2lpVcNqeclWMNLNx48yuN2/L30lWFq6fRuEkOudmvA7p927t6gIhFhevnMHhDCrTGhmRm/CoPB6vV6vF8LhcDgchng8Ho/Hk6363u12u91u/c///HlhAeDVK+mTtra6ukz0bCAQCAQCIm38fr/f79evp6Ojvh6E4MgRq1XnjT0ej8fjSd/on7hcLpfLpU+XzNGFoKxM79yVQ9S44VAoFAqF9OlKxKhdu3JydBqWc9O44VgsFovF9OnKz8/NBSG0bLm2E+biYrkf1UUkEolEIsbvE41Go9GoPl3FxQUFANqDlgo2RnE4HA6HIwNBS26s9S8DanlJF5/P5/P5MrgsTU5evpzJTMfpdDqdzmTUVcFItcFgMBgMCmG32+12e+Z0vHzZ3AxCJFJLlYJl6oHZav9KLVVxrLW1tpYdSEeHrIWZzSYTpOyWrl6VxbF9+2TNaLtjtVosAM3N0pciYVhVAfv7ZQpvMske2W4o3cpHQUFu7qqGFadPHzoE0NXV0JBt8Zuhu/vYMYDGxoMHV/t9zUzL7z95EtIvg2aLpqbqaoDr10+c+Nf/1jSshsbjx+fPA1y7JnvufxnqSkdPz/HjAI8enTu3EX3r5tIquvX2njoFMDh44QIkC+JbjXruyMjFiwA3bsiRuNEXYfio5cGDqSmAu3cnJiBZYdCFXEehs7O+HuDSJZsNtvCoZS1U4V6VUkZH1WHau3cA09OzswBzc9+/p15nsezeDXDggDxMs9l+P0yTuX5ypBnlF8EPpFRyRlqpAAAAAElFTkSuQmCC);
 color: Black;
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
        <td style="white-space: nowrap; padding-right: 20px; border-width: 0px 0px 0px 0px;"> </td>
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
          <xsl:variable name="description" select="description"/>
          <td style="white-space: nowrap; padding-right: 20px; border-width: 0px 0px 0px 0px; text-align: right;">
             &#160;<xsl:value-of select="$description"/>
          </td>
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
        <td style="white-space: nowrap; padding-right: 20px; border-width: 0px 0px 0px 0px;"> </td>
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
