<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!-- ********************************************************************
     An identity style sheet to copy all empty elements and content to output
     ********************************************************************
                   Copyright Panageotech 2010
     ******************************************************************** -->

<!-- ==================================================================== -->
<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" omit-xml-declaration="no"/>

<!-- identity template -->
<xsl:template match="@*|node()">
    <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
</xsl:template>
</xsl:stylesheet>