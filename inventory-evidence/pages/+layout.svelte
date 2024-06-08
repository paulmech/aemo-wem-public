<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	export let data;
</script>

<EvidenceDefaultLayout {data} maxWidth="1400" logo="/tind-logo.jpg" 
	builtWithEvidence="true" githubRepo="https://github.com/paulmech/aemo-wem-public">
	
	<slot slot="content" />
</EvidenceDefaultLayout>
