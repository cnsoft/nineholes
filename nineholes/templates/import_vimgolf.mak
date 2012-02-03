<%inherit file="local:templates.master"/>

<%def name="title()">
  Welcome to TurboGears 2.1, standing on the shoulders of giants, since 2007
</%def>

${parent.sidebar_top()}

<h1>In File</h1>
${file_in | n}

<h1>Out File</h1>
${file_out | n}

<%def name="sidebar_bottom()"></%def>
