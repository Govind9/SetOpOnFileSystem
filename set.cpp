#include<iostream>
#include <boost/filesystem.hpp>
#include<vector>
#include <algorithm> 
namespace fs = boost::filesystem;

using namespace std;

int main(int argc, char *argv[]) {

	vector<string> spathvector;
	vector<string> dpathvector;
	vector<string>::iterator it;
	fs::path source(argc>1? argv[1] : ".");
	fs::path destination(argc>3? argv[3] : ".");
	if(is_directory(source)) {
		std::cout << source << " is a directory containing:\n";
		for(auto& entry :fs::directory_iterator(source)){
			spathvector.push_back(fs::basename(entry)+fs::extension( entry));
		}
	}
	if(is_directory(destination)) {
		std::cout << destination << " is a directory containing:\n";
		for(auto& entry :fs::directory_iterator(destination)){
			dpathvector.push_back(fs::basename(entry)+fs::extension( entry));
		}
	}

	string op(argc>2? argv[2] : "-i");
	string optype;
	vector<string> v;
	if(op=="-d"){
		v.resize(spathvector.size());
		it=std::set_difference (spathvector.begin(), spathvector.end(), dpathvector.begin(), dpathvector.end(), v.begin());
		optype="difference";
	}
	else if(op=="-i"){
		v.resize(spathvector.size()>dpathvector.size()? spathvector.size():dpathvector.size());
		it=std::set_intersection(spathvector.begin(), spathvector.end(), dpathvector.begin(), dpathvector.end(), v.begin());
		optype="intersection";
	}
	else if(op=="-u"){
		v.resize(spathvector.size()+dpathvector.size());
		it=std::set_union(spathvector.begin(), spathvector.end(), dpathvector.begin(), dpathvector.end(), v.begin());
		optype="union";
	}
	else if(op=="-sd"){
		v.resize(spathvector.size()+dpathvector.size());
		it=std::set_symmetric_difference(spathvector.begin(), spathvector.end(), dpathvector.begin(), dpathvector.end(), v.begin());
		optype="symmetric_difference";
	}
	else {
		cout<<"wrong operation";
		return 0;
	}

	v.resize(it-v.begin());
	std::cout << "The "<<optype<<" has " << (v.size()) << " elements:\n";
	for (it=v.begin(); it!=v.end(); ++it){
		std::cout << ' ' << *it;
		std::cout << '\n';
	}
}
