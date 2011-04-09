<%inherit file="base.mako"/>
<%def name="extrajavascript()">
% if extra_context['miniNum']:
 <script type="text/javascript">
        window.location="#${extra_context['miniNum']}";
 </script>
% endif
</%def>
<%def name="body()">
  % if barcode:
    <DIV style="border: solid 1px #999999; padding: 5px; margin: 8px; background: #f2f2f2; width:780px" > 
    <small>Keying using barcode:</small> <B> ${barcode} </B>
    </DIV>
	%endif
  % if alert:
		<div class="error" style="padding: 10px; border: solid 1px red; background: #ffccdd" >
      ${alert}
		</div>
  % endif
	% if form_has_errors:
		<div class="error" style="padding: 10px; border: solid 1px red; background: #ffccdd" >
			Your form could not be submitted due to errors, please scroll down to find the error.
		</div>
	% endif
	<FORM method="post" action="">
		${page}
    
    % if hiddenFields is not UNDEFINED:
      % for key,val in hiddenFields:
        <INPUT TYPE="hidden" VALUE="${val}" NAME="${key}"/>
      % endfor 
      <% hFields = "|^|".join([ x[0] for x in hiddenFields ]) %>\
      <INPUT TYPE="hidden" VALUE="${hFields}" NAME="hFields"/>
    % endif

    <BR>
	  <INPUT type='submit'>
  </FORM>
</%def>

