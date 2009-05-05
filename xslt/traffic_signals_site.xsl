<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="1.0" encoding="iso-8859-1" indent="yes"/>
<xsl:template match="/">
<div class="traffic-signal-site">
 
<h4>Site: <xsl:value-of select="/traffic_signals/site/address"/></h4>

<h5>Phases</h5>
  <xsl:for-each select="//traffic_signals/site/phases/phase">
    <xsl:sort select="letter"/>
    <h6><xsl:value-of select="letter" />&#160;</h6>
    <xsl:if test="string-length(description) &gt; 0" >
      <h6>(<xsl:value-of select="description" />)</h6>
    </xsl:if>
    <p>Phase type: <xsl:value-of select="signal_type" />.</p>
    <xsl:if test="string-length(mintime) &gt; 0" >
       <p>Minimum green running time: <xsl:value-of select="mintime" /></p>
    </xsl:if>
    <xsl:if test="string-length(black_out) &gt; 0" >
       <p>Black out period: <xsl:value-of select="black_out" /></p>
    </xsl:if>
    <xsl:if test="string-length(post_green_time) &gt; 0" >
       <p>Post Green Time: <xsl:value-of select="post_green_time" /></p>
    </xsl:if>
  </xsl:for-each>
  
<h5>Stages</h5>
  <xsl:for-each select="//traffic_signals/site/stages/stage">
    <xsl:sort select="stage_number"/>
    <xsl:variable name="sn" select="stage_number"/>
    <p>Stage <xsl:value-of select="stage_number" />
    <xsl:variable name="ph"  select="//traffic_signals/site/stages/stage[stage_number=$sn]/phases" />
      runs phases: <xsl:value-of select="$ph" />
    </p>
  </xsl:for-each>

<h5>Intergreen table</h5>
<table>
<tr>
<td>&#160;</td>
<xsl:for-each select="//traffic_signals/site/phases/phase">
 <td>&#160;<xsl:value-of select="letter" />&#160;</td>
</xsl:for-each>
</tr>
<xsl:for-each select="//traffic_signals/site/phases/phase">
 <xsl:sort select="letter"/>
 <xsl:variable name="row" select="letter"/>
 <tr><td><xsl:value-of select="letter" /></td>
 <xsl:for-each select="//traffic_signals/site/phases/phase">
    <xsl:sort select="letter"/>
    <xsl:variable name="col" select="letter"/>
    <xsl:variable name="ig" select="//traffic_signals/site/intergreens/intergreen[from=$row and to=$col]/length"/>
    <xsl:if test="string-length($ig) &gt; 1" >
       <td><xsl:value-of select="$ig" />&#160;</td>
    </xsl:if>
    <xsl:if test="string-length($ig) = 1" >
       <td>&#160;<xsl:value-of select="$ig" />&#160;</td>
    </xsl:if>
    <xsl:if test="string-length($ig) &lt; 1" >
       <xsl:if test="$row = $col" >
         <td>&#160;X&#160;</td>
       </xsl:if>
       <xsl:if test="$row != $col" >
         <td>&#160;-&#160;</td>
       </xsl:if>
    </xsl:if>
 </xsl:for-each>
 </tr>
</xsl:for-each>
</table>

<h5>Phase Delays</h5>
  <xsl:variable name="phase_delays_all" select="//traffic_signals/site/phase_delays/phase_delay" />
  <xsl:if test="string-length($phase_delays_all) &lt; 1" >
     <p>No phase delays&#160;</p>
  </xsl:if>  
  <xsl:for-each select="//traffic_signals/site/phase_delays/phase_delay">
    <p>
    Phase <xsl:value-of select="phase" />&#160; 
    on a move from <xsl:value-of select="from" />&#160;
    to <xsl:value-of select="to" />&#160;
    delayed by <xsl:value-of select="length" />&#160;
    </p>
  </xsl:for-each>
</div>
</xsl:template>
</xsl:stylesheet>
