
angular.module("myapp.directives", [])

.directive("myFileInput", [function() {
	return {
		scope: {
			file: '='
		},
		restrict: 'E',
		template: '<input type="file" name="zipzip" />',
		link: function(scope, element, attributes) {
			element.bind("change", function(event) {
				var file = event.target.files[0];
				scope.file = file;
				console.log(file);
			});
		}
	}
}]);