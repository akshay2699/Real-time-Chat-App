<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Company;
use DataTables;
use Validator;
use Mail;
use App\Mail\NewUserNotification;

class CompanyController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index(Request $request)
    {
        if ($request->ajax()) {
            $data = Company::select('*');
            return Datatables::of($data)
                    ->addIndexColumn()
                    ->addColumn('actions', function($row){

                    $btn= '<a href="javascript:void(0)" data-toggle="tooltip" data-id="'.$row->id.'" data-original-title-="Edit" class="edit btn btn-primary editCompany mr-2" id="editCompany">Edit</a>';

                    $btn.= '<a href="javascript:void(0)" data-toggle="tooltip" data-id="'.$row->id.'" data-original-title-="Delete" class="edit btn btn-danger deleteCompany" id="deleteCompany">Delete</a>';    
                            
                    return $btn;
                    })
                    ->rawColumns(['actions'])
                    ->make(true);
        }
        
        return view('admin.company.index');
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        return view('admin.company.create');
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $validator = Validator::make($request->all(),[
            'name'      => 'required',
            'email'     => 'required|email',
            'logo'      => 'image|mimes:jpeg,png,jpg',
            'website'   => 'required',     
        ]);
        if (!$validator->passes()) {
            return response()->json(['error'=>$validator->errors()->all()]);
        }
            
        $companyId = $request->company_id;
     
        $details = [
            'name' => $request->name,
            'email' => $request->email,
            'website' => $request->website
        ];
     
        if ($files = $request->file('logo')) {
         
           //insert new file
           $destinationPath = 'images/'; // upload path
           $profileImage = date('YmdHis') . "." . $files->getClientOriginalExtension();
           $files->move($destinationPath, $profileImage);
           $details['logo'] = "$profileImage";
        }
         
        $company = Company::updateOrCreate(['id' => $companyId], $details);  
        
        $emailAddress = $request->email;
        Mail::to($emailAddress)->send(new NewUserNotification);

        // $data = ['name' => $request->name, 'email' => $request->email];
        // $user['to'] = $request->email;

        // Mail::send('admin.company.mail', $data, function($message) use($user){
        //     $message->to($user['to']);
        //     $message->subject('Subject of mail');
        // });
        return response()->json(['success'=>'Company saved successfully.']);
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        $company = Company::find($id);
        return response()->json($company);
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        Company::find($id)->delete();
        return response()->json(['success'=>'Company deleted successfully.']);
    }
}
