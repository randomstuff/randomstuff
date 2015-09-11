<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:fn="http://www.w3.org/2005/xpath-functions"
		xmlns:err="http://www.w3.org/2005/xqt-errors"
		xmlns:html="http://www.w3.org/1999/xhtml"
		xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
		xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
		xmlns="http://www.w3.org/1999/xhtml"
		>

  <!-- Generate HTML from OpenDocument plain XML for spreadsheets (.fods)

       Normal spreadsheets are zip files and can be processed with:

         unzip -p doo.ods content.xml | saxon-xslt - fods2html.xsl
  -->

  <xsl:strip-space elements="*" />
  <xsl:output method="html" indent="yes" />

  <xsl:template match="/">
    <html>
      <style>
	th { font-weight: bold; }
	td { text-align: right; }
      </style>
      <body>
	<xsl:apply-templates select="//table:table"/>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="@*">
  </xsl:template>

  <xsl:template match="*">
    <xsl:apply-templates select="node()"/>
  </xsl:template>

  <xsl:template match="table:table">
    <table>
      <thead>
	<xsl:apply-templates select="table:table-row[1]"/>
      </thead>
      <tbody>
	<xsl:apply-templates select="table:table-row[position()>1]"/>
      </tbody>
    </table>
  </xsl:template>

  <xsl:template match="table:table-row">
    <tr>
      <xsl:apply-templates select="*"/>
    </tr>
  </xsl:template>

  <xsl:template match="table:table-cell">
    <td>
      <xsl:apply-templates select="node()"/>
    </td>
  </xsl:template>

  <xsl:template match="table:table-row[1]/table:table-cell">
    <th>
      <xsl:apply-templates select="node()"/>
    </th>
  </xsl:template>

</xsl:stylesheet>
